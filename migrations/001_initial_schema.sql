-- ==============================================================================
-- OLMOS GOLD JEWELLERY — Production Relational Database Schema (PostgreSQL 16+)
-- Migration 001: Initial Core Schema (Products, Inventory, Orders, CRM, Audit)
-- Status: Draft / Migration Proposal (DO NOT EXECUTE DIRECTLY IN PRODUCTION)
-- ==============================================================================

-- 1. EXTENSIONS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. BRANCHES / BOUTIQUES (Multi-tenancy / Multi-branch)
CREATE TABLE IF NOT EXISTS boutiques (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(32) NOT NULL UNIQUE, -- e.g. 'CHILONZOR_FLAGSHIP'
    name_uz VARCHAR(255) NOT NULL,
    name_ru VARCHAR(255) NOT NULL,
    address_street VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL DEFAULT 'Tashkent',
    phone VARCHAR(32) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. PRODUCT CATEGORIES (Hierarchical: Rings, Necklaces, Bracelets, Earrings)
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(64) NOT NULL UNIQUE,
    name_uz VARCHAR(100) NOT NULL,
    name_ru VARCHAR(100) NOT NULL,
    parent_id UUID REFERENCES categories(id) ON DELETE RESTRICT,
    display_order INT NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. PRODUCTS (Core Catalog)
-- Money is stored in CENTS / TIYIN (integer) or NUMERIC(14, 2) to prevent IEEE-754 float precision issues
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(64) NOT NULL UNIQUE, -- e.g. 'OLM-MRQ-01'
    category_id UUID NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    title JSONB NOT NULL, -- {"uz": "...", "ru": "...", "en": "..."} for seamless i18n
    description JSONB NOT NULL, -- {"uz": "...", "ru": "..."}
    base_price_cents BIGINT NOT NULL CHECK (base_price_cents > 0), -- USD Cents (e.g. 67300 = $673.00)
    compare_price_cents BIGINT CHECK (compare_price_cents IS NULL OR compare_price_cents >= base_price_cents),
    gold_purity VARCHAR(32) NOT NULL DEFAULT '18K_750', -- '18K_750', '14K_585'
    gold_weight_grams NUMERIC(8, 3) NOT NULL CHECK (gold_weight_grams > 0),
    diamond_specs JSONB, -- {"central_cut": "Marquise", "color": "D-F", "clarity": "VVS1", "side_carat": 0.25}
    has_customizer BOOLEAN NOT NULL DEFAULT FALSE,
    customizer_schema JSONB, -- Carat multipliers and metal alloy matrix
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    deleted_at TIMESTAMPTZ NULL, -- Soft delete support
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Composite Index for fast luxury catalog filtering and sorting
CREATE INDEX IF NOT EXISTS idx_products_category_price ON products (category_id, is_active, base_price_cents) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_products_sku ON products (sku);
CREATE INDEX IF NOT EXISTS idx_products_title_jsonb ON products USING GIN (title);

-- 5. PRODUCT MEDIA (Multi-angle studio photography)
CREATE TABLE IF NOT EXISTS product_images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    image_url VARCHAR(512) NOT NULL,
    caption_uz VARCHAR(255),
    caption_ru VARCHAR(255),
    display_order INT NOT NULL DEFAULT 0,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_product_images_product ON product_images (product_id, display_order);

-- 6. INVENTORY / STOCK PER BOUTIQUE (Real-time physical stock)
CREATE TABLE IF NOT EXISTS boutique_inventory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    boutique_id UUID NOT NULL REFERENCES boutiques(id) ON DELETE RESTRICT,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    ring_size NUMERIC(4, 1) NULL, -- e.g. 16.5, 17.0
    metal_type VARCHAR(32) NOT NULL DEFAULT 'YELLOW_GOLD', -- 'YELLOW_GOLD', 'WHITE_GOLD', 'ROSE_GOLD'
    quantity INT NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_boutique_product_variant UNIQUE (boutique_id, product_id, ring_size, metal_type)
);

-- 7. CUSTOMERS / VIP CRM
CREATE TABLE IF NOT EXISTS customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone VARCHAR(32) NOT NULL UNIQUE, -- Normalized E.164 (e.g. '+998977742021')
    full_name VARCHAR(150),
    telegram_user_id BIGINT UNIQUE,
    telegram_username VARCHAR(64),
    loyalty_tier VARCHAR(32) NOT NULL DEFAULT 'STANDARD', -- 'STANDARD', 'VIP', 'BLACK_DIAMOND'
    notes TEXT,
    is_blacklisted BOOLEAN NOT NULL DEFAULT FALSE,
    anonymized_at TIMESTAMPTZ NULL, -- GDPR/Privacy erasure compliance
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_customers_phone ON customers (phone);
CREATE INDEX IF NOT EXISTS idx_customers_tg_user ON customers (telegram_user_id);

-- 8. LEADS & APPOINTMENTS (VIP fitting and lookbook requests)
CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
    lead_type VARCHAR(32) NOT NULL, -- 'VIP_FITTING', 'LOOKBOOK_DOWNLOAD', 'TELEGRAM_INQUIRY'
    product_id UUID REFERENCES products(id) ON DELETE SET NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'NEW', -- 'NEW', 'CONTACTED', 'APPOINTMENT_SCHEDULED', 'CONVERTED', 'CLOSED'
    assigned_boutique_id UUID REFERENCES boutiques(id) ON DELETE SET NULL,
    details JSONB, -- Additional inputs (name, requested ring size, preferred time)
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_leads_status_created ON leads (status, created_at DESC);

-- 9. ORDERS & TRANSACTIONS
CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(32) NOT NULL UNIQUE, -- e.g. 'OG-2026-10492'
    customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
    boutique_id UUID REFERENCES boutiques(id) ON DELETE RESTRICT,
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'PAID', 'DELIVERED', 'CANCELLED'
    payment_method VARCHAR(32) NOT NULL DEFAULT 'TELEGRAM_CONCIERGE', -- 'PAYME', 'CLICK', 'UZUM', 'CASH', 'TELEGRAM_CONCIERGE'
    total_amount_cents BIGINT NOT NULL CHECK (total_amount_cents >= 0),
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    uzs_exchange_rate NUMERIC(10, 2) NOT NULL DEFAULT 12850.00,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders (customer_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders (status);

-- 10. ORDER ITEMS (Immutable historical snapshot)
-- Products can be updated in the catalog, but past orders must NEVER change price or titles
CREATE TABLE IF NOT EXISTS order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    unit_price_cents BIGINT NOT NULL,
    gold_rate_snapshot NUMERIC(10, 2) NOT NULL,
    item_title_snapshot VARCHAR(255) NOT NULL,
    selected_metal VARCHAR(32) NOT NULL,
    selected_ring_size NUMERIC(4, 1) NULL,
    selected_carat NUMERIC(4, 2) NULL,
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 11. AUDIT TRAIL / SECURITY LOG (Append-only)
CREATE TABLE IF NOT EXISTS audit_logs (
    id BIGSERIAL,
    table_name VARCHAR(64) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(16) NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE'
    performed_by VARCHAR(64),
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Example Monthly Partition for High Performance
CREATE TABLE IF NOT EXISTS audit_logs_2026_10 PARTITION OF audit_logs
    FOR VALUES FROM ('2026-10-01 00:00:00+00') TO ('2026-11-01 00:00:00+00');
