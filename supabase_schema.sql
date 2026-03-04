-- ── SCHEMA SUPABASE PARA SECRETARIA ──────────────────────────────────────

-- Tabla de obras (proyectos)
CREATE TABLE obras (
  id BIGSERIAL PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  constructor_id VARCHAR(255), -- ID de WhatsApp o usuario
  creada_en TIMESTAMP DEFAULT NOW(),
  activa BOOLEAN DEFAULT TRUE
);

-- Tabla de items (materiales/tareas)
CREATE TABLE items (
  id BIGSERIAL PRIMARY KEY,
  obra_id BIGINT REFERENCES obras(id) ON DELETE CASCADE,
  item VARCHAR(500) NOT NULL,
  comprado BOOLEAN DEFAULT FALSE,
  fecha_anotacion TIMESTAMP DEFAULT NOW(),
  fecha_compra TIMESTAMP,
  CONSTRAINT items_obra_fk FOREIGN KEY (obra_id) REFERENCES obras(id)
);

-- Índices para queries rápidas
CREATE INDEX idx_obras_constructor ON obras(constructor_id);
CREATE INDEX idx_items_obra ON items(obra_id);
CREATE INDEX idx_items_comprado ON items(comprado);

-- RLS (Row Level Security) — opcional pero recomendado para producción
ALTER TABLE obras ENABLE ROW LEVEL SECURITY;
ALTER TABLE items ENABLE ROW LEVEL SECURITY;

-- Policy: cada constructor ve solo sus obras
CREATE POLICY "Usuarios ven propias obras"
  ON obras FOR SELECT
  USING (constructor_id = current_setting('app.current_user', true));

-- Policy: cada usuario solo modifica su obra
CREATE POLICY "Usuarios modifican propias obras"
  ON obras FOR UPDATE
  USING (constructor_id = current_setting('app.current_user', true));

-- Policies para items (cascada)
CREATE POLICY "Items solo de propias obras"
  ON items FOR SELECT
  USING (obra_id IN (SELECT id FROM obras WHERE constructor_id = current_setting('app.current_user', true)));

CREATE POLICY "Items solo modifican propia obra"
  ON items FOR UPDATE
  USING (obra_id IN (SELECT id FROM obras WHERE constructor_id = current_setting('app.current_user', true)));

-- ── FIN SCHEMA ──────────────────────────────────────────────────────────────
