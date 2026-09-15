-- ============================================================
-- AulaPay
-- Archivo: 001-schema.sql
--
-- Propósito:
-- Crear el esquema inicial de la base de datos para el backend
-- AulaPay.
--
-- El diseño separa estudiantes, pagos, comprobantes y eventos
-- de auditoría para permitir crecimiento futuro del sistema.
-- ============================================================


-- ============================================================
-- Tabla: students
--
-- Representa a los estudiantes registrados en AulaPay.
--
-- Se utiliza un identificador interno BIGSERIAL como clave
-- primaria y un student_code como identificador funcional.
-- ============================================================

CREATE TABLE IF NOT EXISTS students (
    id BIGSERIAL PRIMARY KEY,

    student_code VARCHAR(32) NOT NULL UNIQUE,

    first_name VARCHAR(100) NOT NULL,

    last_name VARCHAR(100) NOT NULL,

    email VARCHAR(150) NOT NULL UNIQUE,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ============================================================
-- Tabla: payments
--
-- Almacena las transacciones de pago realizadas por los
-- estudiantes.
--
-- NUMERIC se utiliza para valores monetarios para evitar
-- problemas de precisión asociados a tipos FLOAT.
-- ============================================================

CREATE TABLE IF NOT EXISTS payments (
    id BIGSERIAL PRIMARY KEY,

    student_id BIGINT NOT NULL,

    external_reference VARCHAR(64) NOT NULL UNIQUE,

    amount NUMERIC(12, 2) NOT NULL
        CHECK (amount > 0),

    currency CHAR(3) NOT NULL DEFAULT 'USD',

    status VARCHAR(20) NOT NULL
        CHECK (
            status IN (
                'PENDING',
                'PAID',
                'FAILED',
                'REFUNDED'
            )
        ),

    payment_date TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_payments_student
        FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE RESTRICT
);


-- ============================================================
-- Tabla: payment_receipts
--
-- Contiene la metadata asociada a los comprobantes.
--
-- El documento PDF no se almacena dentro de PostgreSQL.
-- Únicamente se registra su ubicación y metadata necesaria.
-- Esto permitirá migrar posteriormente a almacenamiento de
-- objetos como S3, MinIO o servicios equivalentes.
-- ============================================================

CREATE TABLE IF NOT EXISTS payment_receipts (
    id BIGSERIAL PRIMARY KEY,

    payment_id BIGINT NOT NULL UNIQUE,

    file_name VARCHAR(255) NOT NULL,

    storage_path VARCHAR(500) NOT NULL,

    content_type VARCHAR(100) NOT NULL
        DEFAULT 'application/pdf',

    checksum_sha256 CHAR(64),

    generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_payment_receipts_payment
        FOREIGN KEY (payment_id)
        REFERENCES payments(id)
        ON DELETE CASCADE
);


-- ============================================================
-- Tabla: audit_events
--
-- Registra eventos relevantes de seguridad y operación.
--
-- JSONB permite almacenar metadata adicional sin necesidad de
-- modificar el esquema para cada nuevo tipo de evento.
-- ============================================================

CREATE TABLE IF NOT EXISTS audit_events (
    id BIGSERIAL PRIMARY KEY,

    event_type VARCHAR(100) NOT NULL,

    actor_type VARCHAR(50),

    actor_id VARCHAR(100),

    resource_type VARCHAR(50),

    resource_id VARCHAR(100),

    request_id UUID,

    ip_address INET,

    metadata JSONB,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ============================================================
-- Índices
--
-- Mejoran las consultas más frecuentes sin crear índices
-- innecesarios sobre cada columna de las tablas.
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_payments_student_id
    ON payments(student_id);

CREATE INDEX IF NOT EXISTS idx_payments_status
    ON payments(status);

CREATE INDEX IF NOT EXISTS idx_payments_payment_date
    ON payments(payment_date);

CREATE INDEX IF NOT EXISTS idx_audit_events_actor
    ON audit_events(actor_type, actor_id);

CREATE INDEX IF NOT EXISTS idx_audit_events_created_at
    ON audit_events(created_at);
