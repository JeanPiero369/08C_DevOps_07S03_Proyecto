package com.example.hackathon;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.postgresql.PostgreSQLContainer;
import tools.jackson.databind.JsonNode;
import tools.jackson.databind.json.JsonMapper;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

/** Real HTTP, security filters, JSON and JPA against an isolated PostgreSQL database. */
@Testcontainers
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class BootMigrationTest {
    @Container
    static final PostgreSQLContainer DATABASE = new PostgreSQLContainer("postgres:13-alpine");
    private static final String SIGNING_KEY = UUID.randomUUID() + "-" + UUID.randomUUID();
    private static final String INVITATION = UUID.randomUUID().toString();
    private final JsonMapper json = JsonMapper.builder().build();
    private final HttpClient client = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(10)).build();

    @LocalServerPort
    int port;

    @DynamicPropertySource
    static void isolatedConfiguration(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", DATABASE::getJdbcUrl);
        registry.add("spring.datasource.username", DATABASE::getUsername);
        registry.add("spring.datasource.password", DATABASE::getPassword);
        registry.add("jwt.secret", () -> SIGNING_KEY);
        registry.add("teacher.invite-code", () -> INVITATION);
        registry.add("spring.mail.username", () -> "unused@example.test");
        registry.add("spring.mail.password", () -> "");
    }

    private HttpResponse<String> request(String method, String path, Object body, String token) throws Exception {
        HttpRequest.Builder builder = HttpRequest.newBuilder(URI.create("http://localhost:" + port + path))
                .timeout(Duration.ofSeconds(20)).header("Content-Type", "application/json");
        if (token != null) builder.header("Authorization", "Bearer " + token);
        builder.method(method, body == null ? HttpRequest.BodyPublishers.noBody()
                : HttpRequest.BodyPublishers.ofString(json.writeValueAsString(body)));
        return client.send(builder.build(), HttpResponse.BodyHandlers.ofString());
    }

    private Map<String, String> registration(String role) {
        Map<String, String> body = new HashMap<>(Map.of("name", "Migration", "last_name", "Test",
                "email", UUID.randomUUID() + "@example.test", "password", UUID.randomUUID().toString(),
                "role", role));
        if (role.equals("TEACHER")) body.put("invite_code", INVITATION);
        return body;
    }

    private String register(Map<String, String> body) throws Exception {
        HttpResponse<String> response = request("POST", "/auth/register", body, null);
        assertEquals(200, response.statusCode(), "Registration failed");
        String token = json.readTree(response.body()).path("token").asString();
        assertFalse(token.isBlank());
        return token;
    }

    @Test
    void authenticationAndSerializationRemainCompatible() throws Exception {
        Map<String, String> user = registration("STUDENT");
        register(user);
        HttpResponse<String> login = request("POST", "/auth/login",
                Map.of("email", user.get("email"), "password", user.get("password")), null);
        assertEquals(200, login.statusCode());
        String token = json.readTree(login.body()).path("token").asString();
        HttpResponse<String> profile = request("GET", "/student/me", null, token);
        assertEquals(200, profile.statusCode());
        JsonNode data = json.readTree(profile.body());
        assertEquals(user.get("email"), data.path("email").asString());
        assertEquals("STUDENT", data.path("role").asString());
        assertFalse(data.has("password"), "Jackson must never serialize the password hash");
        assertEquals(403, request("GET", "/student/me", null, null).statusCode());
        assertEquals(403, request("POST", "/auth/validate-token", null, token + "tampered").statusCode());
    }

    @Test
    void teacherInvitationAndServerAssignedRoleRemainEnforced() throws Exception {
        String adminAttempt = register(registration("ADMIN"));
        JsonNode claims = json.readTree(request("GET", "/auth/claims", null, adminAttempt).body());
        assertEquals("STUDENT", claims.path("role").asString());
        Map<String, String> teacher = registration("TEACHER");
        teacher.remove("invite_code");
        assertEquals(403, request("POST", "/auth/register", teacher, null).statusCode());
        teacher.put("invite_code", INVITATION);
        String token = register(teacher);
        assertEquals(200, request("GET", "/teacher/me", null, token).statusCode());
    }

    @Test
    void profilePatchCannotChangePrivilegesOrCredentials() throws Exception {
        for (String role : new String[]{"STUDENT", "TEACHER"}) {
            Map<String, String> user = registration(role);
            String token = register(user);
            String path = "/" + role.toLowerCase(java.util.Locale.ROOT) + "/me";
            HttpResponse<String> response = request("PATCH", path,
                    Map.of("name", "Updated", "role", "ADMIN", "coin_available", 99999,
                            "password", UUID.randomUUID().toString()), token);
            assertEquals(200, response.statusCode(), role);
            JsonNode profile = json.readTree(response.body());
            assertEquals("Updated", profile.path("name").asString());
            assertEquals(role, profile.path("role").asString());
            assertNotEquals(99999, profile.path("coin_available").asInt());
            assertFalse(profile.has("password"));
            assertEquals(200, request("POST", "/auth/login",
                    Map.of("email", user.get("email"), "password", user.get("password")), null).statusCode());
        }
    }
}
