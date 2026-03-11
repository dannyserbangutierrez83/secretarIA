-- ── MIGRACIÓN: Múltiples obras por usuario ──────────────────────────────────
-- Ejecutar en Supabase SQL Editor

-- 1. Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    telegram_id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    obra_activa_id BIGINT REFERENCES obras(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Quitar columna activa de obras (ya no se usa)
ALTER TABLE obras DROP COLUMN IF EXISTS activa;

-- 3. Índice para buscar obras por constructor rápido
CREATE INDEX IF NOT EXISTS idx_obras_constructor_id ON obras(constructor_id);

-- ── INSERTAR USUARIOS AUTORIZADOS ────────────────────────────────────────────
-- Reemplazar el telegram_id por el chat.id real de cada usuario
-- (se puede ver en los logs de Railway cuando el usuario escribe al bot)

-- Ejemplo:
-- INSERT INTO usuarios (telegram_id, nombre) VALUES ('123456789', 'Dario');

-- ── FIN MIGRACIÓN ─────────────────────────────────────────────────────────────
