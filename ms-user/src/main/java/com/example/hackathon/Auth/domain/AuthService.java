package com.example.hackathon.Auth.domain;

import com.example.hackathon.Auth.dto.RpJwtAuthtentication;
import com.example.hackathon.Auth.dto.RqUserLoginDto;
import com.example.hackathon.Auth.dto.RqUserRegisterDto;
import com.example.hackathon.Exceptions.ForbiddenException;
import com.example.hackathon.Exceptions.NotFoundException;
import com.example.hackathon.Exceptions.UniqueConstraintException;
import com.example.hackathon.Student.domain.Student;
import com.example.hackathon.Student.infrastructure.StudentRepository;
import com.example.hackathon.Teacher.domain.Teacher;
import com.example.hackathon.Teacher.infrastructure.TeacherRepository;
import com.example.hackathon.Usuario.domain.Role;
import com.example.hackathon.Usuario.domain.Usuario;
import com.example.hackathon.Usuario.infrastructure.UsuarioRepository;

import jakarta.servlet.http.HttpServletRequest;

import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.Date;
import java.util.Map;
import java.util.Optional;

@Service
public class AuthService {
    @Autowired
    UsuarioRepository usuarioRepository;
    
    @Autowired
    TeacherRepository teacherRepository;
    @Autowired
    StudentRepository studentRepository;


    @Autowired
    PasswordEncoder passwordEncoder;
    @Autowired
    JwtService jwtService;
    @Autowired
    private ModelMapper modelMapper;

    /** Código de invitación docente (variable TEACHER_INVITE_CODE). Vacío = registro docente deshabilitado. */
    @Value("${teacher.invite-code:}")
    private String teacherInviteCode;

    public RpJwtAuthtentication login(RqUserLoginDto rqUserDto) {
        Optional<Usuario> user= usuarioRepository.findByEmail(rqUserDto.getEmail());

        if (user.isEmpty()) throw new NotFoundException("Email is not registered");
        if (!passwordEncoder.matches(rqUserDto.getPassword(), user.get().getPassword()))
            throw new IllegalArgumentException("Password is incorrect");

        RpJwtAuthtentication token = new RpJwtAuthtentication();
        token.setToken(jwtService.generateToken(user.get()));
        return token;
    }

    public RpJwtAuthtentication register(RqUserRegisterDto usuario){
        Optional<Usuario> user = usuarioRepository.findByEmail(usuario.getEmail());
        usuario.setPassword(passwordEncoder.encode(usuario.getPassword()));
        if (user.isPresent()) throw new UniqueConstraintException("Email is already registered");

        RpJwtAuthtentication token = new RpJwtAuthtentication();
        usuario.setRegistration_date(new Date());
        // El rol lo decide el servidor, nunca el cliente (E-02): TEACHER solo con un
        // código de invitación válido; cualquier otro caso (incluido ADMIN) es STUDENT.
        usuario.setRole(resolveRole(usuario));
        if(usuario.getRole()==Role.STUDENT){
            Student usuarioNuevo = modelMapper.map(usuario, Student.class);
            studentRepository.save(usuarioNuevo);
            token.setToken(jwtService.generateToken(usuarioNuevo));

        }
        else if (usuario.getRole()==Role.TEACHER){
            Teacher usuarioNuevo = modelMapper.map(usuario, Teacher.class);
            teacherRepository.save(usuarioNuevo);
            token.setToken(jwtService.generateToken(usuarioNuevo));
        }

        return token;
    }
    
    Role resolveRole(RqUserRegisterDto usuario) {
        boolean wantsTeacher = usuario.getRole() == Role.TEACHER
                || (usuario.getInvite_code() != null && !usuario.getInvite_code().isBlank());
        if (!wantsTeacher) {
            return Role.STUDENT;
        }
        if (!isValidInviteCode(usuario.getInvite_code())) {
            throw new ForbiddenException("Código de invitación docente inválido");
        }
        return Role.TEACHER;
    }

    boolean isValidInviteCode(String code) {
        if (teacherInviteCode == null || teacherInviteCode.isBlank() || code == null) {
            return false;
        }
        // Comparación en tiempo constante para no filtrar el código por timing
        return MessageDigest.isEqual(teacherInviteCode.getBytes(StandardCharsets.UTF_8),
                code.trim().getBytes(StandardCharsets.UTF_8));
    }

    /** Extrae el JWT del header Authorization; null si falta o no es Bearer. */
    private String bearerToken(HttpServletRequest request) {
        String authHeader = request.getHeader("Authorization");
        if (authHeader == null || !authHeader.startsWith("Bearer ") || authHeader.length() <= 7) {
            return null;
        }
        return authHeader.substring(7);
    }

    public boolean validate(HttpServletRequest request){
        String jwt = bearerToken(request);
        if (jwt == null) {
            return false;   // antes: substring(7) sobre null -> 500
        }
        try {
            String userEmail = jwtService.extractUsername(jwt);
            return userEmail != null && jwtService.isTokenValid(jwt, userEmail);
        } catch (RuntimeException e) {
            return false;   // token mal formado o usuario inexistente -> 403, no 500
        }
    }

    /** Identidad del token validado, para que el gateway no confíe en ids del cliente (T-01). */
    public Map<String, Object> claims(HttpServletRequest request) {
        if (!validate(request)) {
            return null;
        }
        String email = jwtService.extractUsername(bearerToken(request));
        Optional<Usuario> found = usuarioRepository.findByEmail(email);
        Usuario user = found.orElse(null);
        if (user == null) {
            return null;
        }
        return Map.of("id", user.getId(), "email", user.getEmail(), "role", user.getRole().name());
    }

    public boolean validate(String role, HttpServletRequest request){
        if(!validate(request))
            return false;

        String jwt = bearerToken(request);
        String tokenRole = jwtService.extractRole(jwt);

        if (tokenRole == null || !tokenRole.equalsIgnoreCase(role)){
            return false;
        }

        return true;        
    }
}
