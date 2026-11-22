## Resumen de seguridad

| Herramienta | CRITICAL | HIGH | MEDIUM | LOW | INFO | Total |
|---|---:|---:|---:|---:|---:|---:|
| Bandit | 0 | 0 | 2 | 10 | 0 | 12 |
| Gitleaks | 0 | 46 | 0 | 0 | 0 | 46 |
| OWASP ZAP | 0 | 0 | 3 | 6 | 7 | 16 |
| Semgrep | 0 | 0 | 0 | 0 | 1 | 1 |
| Trivy | 2 | 112 | 282 | 178 | 14 | 588 |
| **Total** | **2** | **158** | **287** | **194** | **22** | **663** |

### Hallazgos CRITICAL / HIGH

| Severidad | Herramienta | Regla | Hallazgo | Ubicación |
|---|---|---|---|---|
| CRITICAL | Trivy | CVE-2026-47884 | org.springframework:spring-webmvc 6.2.19: org.springframework/spring-webmvc: Spring Framework: Remote Code Execution via improper path limitation in XsltView | Java |
| CRITICAL | Trivy | CVE-2026-47890 | org.springframework:spring-webmvc 6.2.19: org.springframework/spring-webmvc: org.springframework/spring-webflux: Spring Framework: Stream corruption in Server-S | Java |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/06-classroom-competence-ranking.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/06-classroom-ranking.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/05-Quiz/02-quiz-student-result.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/02-Student/04-student-quiz-list.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/02-Student/01-student-me.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/04-teacher-classroom-add-users.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/04-teacher-classroom-add-users.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/02-Student/03-student-submit-quiz.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/10-teacher-generate-quiz-from-text.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/02-classroom-all-teacher.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/02-classroom-all-teacher.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/08-teacher-classroom-quiz-create.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/08-teacher-classroom-quiz-create.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/05-teacher-competence.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/01-classroom-all-student.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/01-classroom-all-student.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/07-teacher-classroom-competence-associate.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/01-teacher-me.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/01-teacher-me.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/02-Student/02-student-modify.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/03-teacher-create-classroom.bru:19 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/03-teacher-create-classroom.bru:21 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/03-classroom-by-user-id.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/03-classroom-by-user-id.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/04-classroom-by-id.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/04-classroom-by-id.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/05-Quiz/01-quiz-by-id.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/05-classroom-competences.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/04-Classroom/05-classroom-competences.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/05-Quiz/20-quiz-create-full.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/05-Quiz/Create New Quiz.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/02-teacher-modify.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/06-teacher-competence.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/09-teacher-generate-quiz-from-pdf.bru:15 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/03-Teacher/09-teacher-generate-quiz-from-pdf.bru:17 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-orchestrator/ms-orquestrator/05-Quiz/03-quiz-list.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/01-Auth/03-auth-validate-token.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/01-Auth/04-auth-validate-token-role.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/02-Student/01-student-me.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/02-Student/02-student-by-id.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/02-Student/03-student-ids-by-email.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/02-Student/05-student-buy-character.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/02-Student/04-student-add-coins.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/03-Teacher/01-teacher-me.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/03-Teacher/03-teacher-ids-by-email.bru:14 |
| HIGH | Gitleaks | jwt | Uncovered a JSON Web Token, which may lead to unauthorized access to web applications and sensitive user data. | ms-user/api-endpoints/03-Teacher/02-teacher-by-id.bru:14 |
| HIGH | Trivy | CVE-2026-45623 | postcss 8.4.31: postcss: PostCSS: Information disclosure and denial of service via crafted CSS input | frontend/package-lock.json |
| HIGH | Trivy | CVE-2026-73646 | postcss 8.4.31: postcss: PostCSS: Information disclosure via path traversal in source map auto-loading | frontend/package-lock.json |
| HIGH | Trivy | CVE-2026-54291 | org.postgresql:postgresql 42.7.11: org.postgresql/postgresql: com.ongres.scram/scram-client: pgjdbc: Man-in-the-middle protection bypass via SCRAM-SHA-256-PLUS  | ms-user/pom.xml |
| HIGH | Trivy | CVE-2026-45623 | postcss 8.4.31: postcss: PostCSS: Information disclosure and denial of service via crafted CSS input | Node.js |
| HIGH | Trivy | CVE-2026-73646 | postcss 8.4.31: postcss: PostCSS: Information disclosure via path traversal in source map auto-loading | Node.js |
| HIGH | Trivy | CVE-2026-76642 | bsdutils 1:2.41.5-0+deb13u1: util-linux: util-linux: failed external mount helper still runs privileged X-mount post-hooks | microservice-quiz (debian 13.7) |
| HIGH | Trivy | CVE-2026-78408 | bsdutils 1:2.41.5-0+deb13u1: util-linux: util-linux: nsenter --join-cgroup leaks root cgroup migration authority | microservice-quiz (debian 13.7) |
| HIGH | Trivy | CVE-2026-78409 | bsdutils 1:2.41.5-0+deb13u1: util-linux: util-linux: X-mount.subdir detached-tree resolution can escape via intermediate symlinks | microservice-quiz (debian 13.7) |
| HIGH | Trivy | CVE-2026-78410 | bsdutils 1:2.41.5-0+deb13u1: util-linux: util-linux: restricted bind mounts do not pin the source, allowing X-mount.owner/group/mode redirection | microservice-quiz (debian 13.7) |
| HIGH | Trivy | CVE-2026-54369 | libacl1 2.3.2-2+b1: acl: Symlink traversal privilege escalation via libacl functions | microservice-quiz (debian 13.7) |
| HIGH | Trivy | CVE-2026-76642 | libblkid1 2.41.5-0+deb13u1: util-linux: util-linux: failed external mount helper still runs privileged X-mount post-hooks | microservice-quiz (debian 13.7) |
| HIGH | Trivy | CVE-2026-78408 | libblkid1 2.41.5-0+deb13u1: util-linux: util-linux: nsenter --join-cgroup leaks root cgroup migration authority | microservice-quiz (debian 13.7) |
