/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true, // Ativa modo restrito do react para alertas de possíveis problemas
    images: {
        domains: [] //! Domínios externos permitidos para imagens, se necessário.
    },
    env: {
        API_URL: "http://127.0.0.1:8000", //! URL do backend em FastAPI
    }
};

module.exports = nextConfig;