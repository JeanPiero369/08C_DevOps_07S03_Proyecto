# Etapa 1: construir con Maven
FROM maven:3.9.4-eclipse-temurin-17 AS builder
WORKDIR /app

# pom.xml primero: las dependencias se cachean y no se vuelven a descargar
# cada vez que cambia el código fuente
COPY pom.xml ./
RUN mvn -B dependency:go-offline

COPY src ./src
RUN mvn -B clean package -DskipTests

# Etapa 2: solo el JRE para ejecutar el .jar
FROM eclipse-temurin:17-jre
WORKDIR /app

RUN groupadd -r spring && useradd -r -g spring spring
USER spring:spring

COPY --from=builder --chown=spring:spring /app/target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-XX:MaxRAMPercentage=75", "-jar", "app.jar"]