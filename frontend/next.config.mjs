// .mjs (no .ts): así `next start` no necesita TypeScript en la imagen de producción;
// con .ts, Next intentaba instalarlo con yarn desde internet en cada arranque.

// MED-004 / S-02: cabeceras de seguridad para todas las rutas.
// connect-src debe incluir el gateway (NEXT_PUBLIC_API_URL) al que llama el navegador.
const apiOrigin = (() => {
  try {
    return new URL(process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000').origin;
  } catch {
    return 'http://localhost:8000';
  }
})();

const isDev = process.env.NODE_ENV !== 'production';

const contentSecurityPolicy = [
  "default-src 'self'",
  // Next.js inyecta scripts inline para la hidratación; en dev también necesita eval
  // 'wasm-unsafe-eval': decodificador Draco (WASM) de los modelos 3D de la tienda
  `script-src 'self' 'unsafe-inline' 'wasm-unsafe-eval'${isDev ? " 'unsafe-eval'" : ''}`,
  "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
  "font-src 'self' https://fonts.gstatic.com",
  "img-src 'self' data: blob: https://placehold.co https://mscharacters.s3.us-east-1.amazonaws.com",
  // www.gstatic.com: decodificador Draco que descarga useGLTF
  `connect-src 'self' ${apiOrigin} https://mscharacters.s3.us-east-1.amazonaws.com https://www.gstatic.com${isDev ? ' ws:' : ''}`,
  "worker-src 'self' blob:",
  "frame-ancestors 'none'",
  "base-uri 'self'",
  "form-action 'self'",
  "object-src 'none'",
].join('; ');

const securityHeaders = [
  { key: 'Content-Security-Policy', value: contentSecurityPolicy },
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
  { key: 'Cross-Origin-Opener-Policy', value: 'same-origin' },
];

/** @type {import('next').NextConfig} */
const nextConfig = {
  /* config options here */
  transpilePackages: ['three'], // importante segun documentacion oficial de  https://r3f.docs.pmnd.rs/getting-started/installation
  poweredByHeader: false, // ZAP 10037: no anunciar X-Powered-By
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'placehold.co',
        port: '',
        pathname: '/**',
      },
    ],
  },
  async headers() {
    return [{ source: '/:path*', headers: securityHeaders }];
  },
};

export default nextConfig;
