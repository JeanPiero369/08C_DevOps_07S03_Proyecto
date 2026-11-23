package com.example.hackathon.Auth.domain;

import com.example.hackathon.Auth.dto.RqUserRegisterDto;
import com.example.hackathon.Exceptions.ForbiddenException;
import com.example.hackathon.Usuario.domain.Role;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.test.util.ReflectionTestUtils;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Pruebas unitarias (sin Spring ni base de datos) de los controles de E-02 y del
 * fallo de validate() con header nulo. Se ejecutan con: mvn test -Dtest=AuthServiceSecurityTest
 */
class AuthServiceSecurityTest {

    private AuthService service;

    @BeforeEach
    void setUp() {
        service = new AuthService();
        ReflectionTestUtils.setField(service, "teacherInviteCode", "codigo-docente-123");
    }

    private RqUserRegisterDto dto(Role role, String code) {
        RqUserRegisterDto d = new RqUserRegisterDto();
        d.setRole(role);
        d.setInvite_code(code);
        return d;
    }

    @Test
    void registroSinRolCreaStudent() {
        assertEquals(Role.STUDENT, service.resolveRole(dto(null, null)));
    }

    @Test
    void registroComoStudentCreaStudent() {
        assertEquals(Role.STUDENT, service.resolveRole(dto(Role.STUDENT, null)));
    }

    @Test
    void clienteNoPuedeAutoasignarseAdmin() {
        assertEquals(Role.STUDENT, service.resolveRole(dto(Role.ADMIN, null)));
    }

    @Test
    void teacherSinCodigoEsRechazado() {
        assertThrows(ForbiddenException.class, () -> service.resolveRole(dto(Role.TEACHER, null)));
    }

    @Test
    void teacherConCodigoIncorrectoEsRechazado() {
        assertThrows(ForbiddenException.class, () -> service.resolveRole(dto(Role.TEACHER, "adivinado")));
    }

    @Test
    void teacherConCodigoValidoCreaTeacher() {
        assertEquals(Role.TEACHER, service.resolveRole(dto(Role.TEACHER, "codigo-docente-123")));
    }

    @Test
    void codigoValidoSinRolTambienCreaTeacher() {
        assertEquals(Role.TEACHER, service.resolveRole(dto(null, " codigo-docente-123 ")));
    }

    @Test
    void sinCodigoConfiguradoNadieEsTeacher() {
        ReflectionTestUtils.setField(service, "teacherInviteCode", "");
        assertThrows(ForbiddenException.class, () -> service.resolveRole(dto(Role.TEACHER, "")));
        assertFalse(service.isValidInviteCode(""));
    }

    @Test
    void validateSinHeaderDevuelveFalseEnVezDe500() {
        assertFalse(service.validate(new MockHttpServletRequest()));
    }

    @Test
    void validateConHeaderNoBearerDevuelveFalse() {
        MockHttpServletRequest req = new MockHttpServletRequest();
        req.addHeader("Authorization", "Basic abc");
        assertFalse(service.validate(req));
    }
}
