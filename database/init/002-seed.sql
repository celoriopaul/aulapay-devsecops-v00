-- ============================================================
-- AulaPay
-- Archivo: 002-seed.sql
--
-- Propósito:
-- Crear datos iniciales únicamente para el laboratorio.
--
-- Los estudiantes 1024 y 2048 son importantes porque serán
-- utilizados posteriormente para demostrar la falla de
-- autorización a nivel de objeto solicitada en el reto.
-- ============================================================


-- ============================================================
-- Estudiantes de prueba
-- ============================================================

INSERT INTO students (
    student_code,
    first_name,
    last_name,
    email
)
VALUES
    (
        '1024',
        'Andrea',
        'Mendoza',
        'andrea.mendoza@example.test'
    ),
    (
        '2048',
        'Carlos',
        'Paredes',
        'carlos.paredes@example.test'
    )
ON CONFLICT (student_code) DO NOTHING;


-- ============================================================
-- Pagos del estudiante 1024
-- ============================================================

INSERT INTO payments (
    student_id,
    external_reference,
    amount,
    currency,
    status,
    payment_date
)
SELECT
    id,
    'AULAPAY-2026-000001',
    325.50,
    'USD',
    'PAID',
    NOW() - INTERVAL '10 days'
FROM students
WHERE student_code = '1024'
ON CONFLICT (external_reference) DO NOTHING;


INSERT INTO payments (
    student_id,
    external_reference,
    amount,
    currency,
    status,
    payment_date
)
SELECT
    id,
    'AULAPAY-2026-000002',
    180.00,
    'USD',
    'PAID',
    NOW() - INTERVAL '5 days'
FROM students
WHERE student_code = '1024'
ON CONFLICT (external_reference) DO NOTHING;


-- ============================================================
-- Pago del estudiante 2048
--
-- Este registro permitirá demostrar posteriormente que el
-- usuario 1024 puede consultar información que no le pertenece
-- cuando implementemos deliberadamente la versión vulnerable.
-- ============================================================

INSERT INTO payments (
    student_id,
    external_reference,
    amount,
    currency,
    status,
    payment_date
)
SELECT
    id,
    'AULAPAY-2026-000003',
    450.75,
    'USD',
    'PAID',
    NOW() - INTERVAL '3 days'
FROM students
WHERE student_code = '2048'
ON CONFLICT (external_reference) DO NOTHING;


-- ============================================================
-- Comprobantes
-- ============================================================

INSERT INTO payment_receipts (
    payment_id,
    file_name,
    storage_path,
    checksum_sha256
)
SELECT
    id,
    'AULAPAY-2026-000001.pdf',
    '/receipts/2026/AULAPAY-2026-000001.pdf',
    NULL
FROM payments
WHERE external_reference = 'AULAPAY-2026-000001'
ON CONFLICT (payment_id) DO NOTHING;


INSERT INTO payment_receipts (
    payment_id,
    file_name,
    storage_path,
    checksum_sha256
)
SELECT
    id,
    'AULAPAY-2026-000002.pdf',
    '/receipts/2026/AULAPAY-2026-000002.pdf',
    NULL
FROM payments
WHERE external_reference = 'AULAPAY-2026-000002'
ON CONFLICT (payment_id) DO NOTHING;


INSERT INTO payment_receipts (
    payment_id,
    file_name,
    storage_path,
    checksum_sha256
)
SELECT
    id,
    'AULAPAY-2026-000003.pdf',
    '/receipts/2026/AULAPAY-2026-000003.pdf',
    NULL
FROM payments
WHERE external_reference = 'AULAPAY-2026-000003'
ON CONFLICT (payment_id) DO NOTHING;
