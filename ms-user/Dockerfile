# Etapa 1: construir con Maven
FROM maven:3.9.4-eclipse-temurin-17 AS builder
WORKDIR /app

# Copiar código fuente y empaquetar el jar
COPY pom.xml src ./
RUN mvn dependency:go-offline -B && mvn clean package -DskipTests -B

# Etapa 2: ejecutar el .jar en una imagen liviana (solo JRE)
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# Ejecutar como usuario no root
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

COPY --from=builder --chown=spring:spring /app/target/*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]

