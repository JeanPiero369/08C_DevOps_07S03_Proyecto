## Resumen de seguridad

| Herramienta | CRITICAL | HIGH | MEDIUM | LOW | INFO | Total |
|---|---:|---:|---:|---:|---:|---:|
| Bandit | 0 | 0 | 2 | 10 | 0 | 12 |
| Checkov | 0 | 0 | 3 | 0 | 0 | 3 |
| Gitleaks | 0 | 48 | 0 | 0 | 0 | 48 |
| OWASP ZAP | 0 | 0 | 3 | 11 | 8 | 22 |
| Semgrep | 0 | 46 | 2 | 0 | 1 | 49 |
| Trivy | 33 | 288 | 474 | 254 | 14 | 1063 |
| pip-audit | 0 | 0 | 1 | 0 | 0 | 1 |
| **Total** | **33** | **382** | **485** | **275** | **23** | **1198** |

### Hallazgos CRITICAL / HIGH

| Severidad | Herramienta | Regla | Hallazgo | Ubicación |
|---|---|---|---|---|
| CRITICAL | Trivy | CVE-2026-90711 | proxy-addr 2.0.7: proxy-addr: proxy-addr vulnerable to IP spoofing via IPv4-mapped IPv6 trust subnet | ms-classroom/package-lock.json |
| CRITICAL | Trivy | CVE-2026-31789 | libcrypto3 3.3.3-r0: openssl: OpenSSL: Heap buffer overflow on 32-bit systems from large X.509 certificate processing | frontend (alpine 3.21.3) |
| CRITICAL | Trivy | CVE-2026-31789 | libssl3 3.3.3-r0: openssl: OpenSSL: Heap buffer overflow on 32-bit systems from large X.509 certificate processing | frontend (alpine 3.21.3) |
| CRITICAL | Trivy | CVE-2026-106445 | handlebars 4.7.8: handlebars: Handlebars: JavaScript Injection via Own Property Check Bypass | Node.js |
| CRITICAL | Trivy | CVE-2026-106446 | handlebars 4.7.8: handlebars: Handlebars: JavaScript Injection via AST Type Confusion in compile (Program.blockParams) | Node.js |
| CRITICAL | Trivy | CVE-2026-33937 | handlebars 4.7.8: handlebars.js: Handlebars: Remote Code Execution via crafted Abstract Syntax Tree object in compile() | Node.js |
| CRITICAL | Trivy | CVE-2025-55182 | next 15.3.3: next: React Server Components: Pre-authentication remote code execution via unsafe deserialization | Node.js |
| CRITICAL | Trivy | CVE-2026-75604 | next 15.3.3: next: Next.js: Unauthenticated Remote Code Execution on windows-hosted servers | Node.js |
| CRITICAL | Trivy | GHSA-2464-fhr4-w9xw | next 15.3.3: Next.js: Unauthenticated Remote Code Execution in Image Optimization API when SVG files are used | Node.js |
| CRITICAL | Trivy | GHSA-2xp9-vwfh-vxw4 | next 15.3.3: Next.js: Unauthenticated Remote Code Execution in Image Optimization API when AVIF files are used | Node.js |
| CRITICAL | Trivy | CVE-2026-41242 | protobufjs 7.5.3: protobufjs: protobufjs: Arbitrary code execution via injected protobuf definition type fields | Node.js |
| CRITICAL | Trivy | CVE-2026-90711 | proxy-addr 2.0.7: proxy-addr: proxy-addr vulnerable to IP spoofing via IPv4-mapped IPv6 trust subnet | Node.js |
| CRITICAL | Trivy | CVE-2026-59873 | tar 6.2.1: tar: node-tar: Denial of Service via crafted gzip bomb | Node.js |
| CRITICAL | Trivy | CVE-2026-54466 | websocket-driver 0.7.4: websocket-driver is a WebSocket protocol handler with pluggable I/O. P ... | Node.js |
| CRITICAL | Trivy | CVE-2026-90711 | proxy-addr 2.0.7: proxy-addr: proxy-addr vulnerable to IP spoofing via IPv4-mapped IPv6 trust subnet | Node.js |
| CRITICAL | Trivy | CVE-2026-59873 | tar 6.2.1: tar: node-tar: Denial of Service via crafted gzip bomb | Node.js |
| CRITICAL | Trivy | CVE-2025-24813 | org.apache.tomcat.embed:tomcat-embed-core 10.1.24: tomcat: Potential RCE and/or information disclosure and/or information corruption with partial PUT | Java |
| CRITICAL | Trivy | CVE-2026-41293 | org.apache.tomcat.embed:tomcat-embed-core 10.1.24: tomcat-coyote: Apache Tomcat: HTTP/2 request headers not validated | Java |
| CRITICAL | Trivy | CVE-2026-43512 | org.apache.tomcat.embed:tomcat-embed-core 10.1.24: tomcat-coyote: Apache Tomcat: Authentication bypass via digest authentication | Java |
| CRITICAL | Trivy | CVE-2026-43515 | org.apache.tomcat.embed:tomcat-embed-core 10.1.24: tomcat-coyote: tomcat: Improper Authorization allows security bypass | Java |
| CRITICAL | Trivy | CVE-2026-55276 | org.apache.tomcat.embed:tomcat-embed-core 10.1.24: tomcat: Apache Tomcat: Misleading security logs due to incorrect control flow | Java |
| CRITICAL | Trivy | CVE-2026-65182 | org.apache.tomcat.embed:tomcat-embed-core 10.1.24: tomcat: Apache Tomcat: Security constraint bypass due to improper access control | Java |
| CRITICAL | Trivy | CVE-2026-65905 | org.apache.tomcat.embed:tomcat-embed-core 10.1.24: tomcat: Apache Tomcat: Authentication bypass via limited replay attack in DIGEST authenticator | Java |
| CRITICAL | Trivy | CVE-2026-68525 | org.apache.tomcat.embed:tomcat-embed-core 10.1.24: tomcat: Apache Tomcat: Unauthorized resource access via FORM authentication bypass | Java |
| CRITICAL | Trivy | CVE-2024-38821 | org.springframework.security:spring-security-web 6.3.0: Spring-WebFlux: Authorization Bypass of Static Resources in WebFlux Applications | Java |
| CRITICAL | Trivy | CVE-2026-22732 | org.springframework.security:spring-security-web 6.3.0: Spring Security: Spring Security: Security policy bypass and information disclosure due to unwritten HTT | Java |
| CRITICAL | Trivy | CVE-2026-47884 | org.springframework:spring-webmvc 6.1.8: org.springframework/spring-webmvc: Spring Framework: Remote Code Execution via improper path limitation in XsltView | Java |
| CRITICAL | Trivy | CVE-2026-40477 | org.thymeleaf:thymeleaf 3.1.2.RELEASE: thymeleaf: Thymeleaf: Server-Side Template Injection via security bypass in expression execution | Java |
| CRITICAL | Trivy | CVE-2026-40478 | org.thymeleaf:thymeleaf 3.1.2.RELEASE: thymeleaf: Thymeleaf: Server-Side Template Injection via expression execution bypass | Java |
| CRITICAL | Trivy | CVE-2026-41901 | org.thymeleaf:thymeleaf 3.1.2.RELEASE: thymeleaf: Thymeleaf: Server-Side Template Injection (SSTI) via expression execution bypass | Java |
| CRITICAL | Trivy | CVE-2026-40477 | org.thymeleaf:thymeleaf-spring6 3.1.2.RELEASE: thymeleaf: Thymeleaf: Server-Side Template Injection via security bypass in expression execution | Java |
| CRITICAL | Trivy | CVE-2026-40478 | org.thymeleaf:thymeleaf-spring6 3.1.2.RELEASE: thymeleaf: Thymeleaf: Server-Side Template Injection via expression execution bypass | Java |
| CRITICAL | Trivy | CVE-2026-41901 | org.thymeleaf:thymeleaf-spring6 3.1.2.RELEASE: thymeleaf: Thymeleaf: Server-Side Template Injection (SSTI) via expression execution bypass | Java |
| HIGH | Gitleaks | aws-access-token | Identified a pattern that may indicate AWS credentials, risking unauthorized cloud resource access and data breaches on AWS platforms. | docs/devsecops/baseline/pip-audit-ms-quiz.json:1 |
| HIGH | Gitleaks | aws-access-token | Identified a pattern that may indicate AWS credentials, risking unauthorized cloud resource access and data breaches on AWS platforms. | docs/devsecops/baseline/pip-audit-ms-quiz.json:1 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/02-teacher-modify.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/06-classroom-ranking.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/05-Quiz/02-quiz-student-result.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/05-Quiz/01-quiz-by-id.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/02-Student/01-student-me.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/02-Student/03-student-submit-quiz.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/02-Student/04-student-quiz-list.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/05-teacher-competence.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/07-teacher-classroom-competence-associate.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/06-teacher-competence.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/09-teacher-generate-quiz-from-pdf.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/09-teacher-generate-quiz-from-pdf.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/10-teacher-generate-quiz-from-text.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/08-teacher-classroom-quiz-create.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/08-teacher-classroom-quiz-create.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/02-classroom-all-teacher.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/02-classroom-all-teacher.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/04-classroom-by-id.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/04-classroom-by-id.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/03-classroom-by-user-id.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/03-classroom-by-user-id.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/06-classroom-competence-ranking.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/05-Quiz/03-quiz-list.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/05-Quiz/Create New Quiz.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/05-Quiz/20-quiz-create-full.bru:14 |
