-- Create MVP unknown asset kinds table (temporary) with complete structure
CREATE TABLE IF NOT EXISTS public.mvp_asset_kinds (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Copy all data from asset_kinds, preserving the original IDs
INSERT INTO public.mvp_asset_kinds (id, name, created_at, updated_at)
SELECT id, name, created_at, updated_at FROM public.asset_kinds;

-- Set the sequence to continue from the next available ID
SELECT setval('mvp_asset_kinds_id_seq', (SELECT MAX(id) FROM public.asset_kinds));

CREATE TABLE IF NOT EXISTS public.mvp_asset_less_resources (
	id BIGSERIAL PRIMARY KEY NOT NULL,
    resource_id BIGINT,
    url TEXT,
	kind_name TEXT,
	kind_id INT NULL
);

-- MVP resources without assets
WITH mvp_resources_without_assets AS (
    SELECT mvp.resource_id,mvp.deeplink as url,LOWER(r.resource_type) as kind_name,ak.id AS kind_id
    FROM public.mvp_downloader_library mvp
    INNER JOIN public.resources r ON mvp.resource_id = r.id
    LEFT JOIN public.asset_resource ar ON mvp.resource_id = ar.resource_id
    LEFT JOIN public.asset_kinds ak ON r.resource_type = ak.name
    WHERE ar.resource_id IS NULL
)

-- Filling temporary table
INSERT INTO public.mvp_asset_less_resources (resource_id, url, kind_name, kind_id)
SELECT resource_id, url, kind_name, kind_id FROM mvp_resources_without_assets;

WITH unknown_asset_kinds AS (
    SELECT kind_name
    FROM mvp_asset_less_resources
    WHERE kind_id IS NULL
    GROUP BY kind_name
)

-- Insert asset kinds when they are not in the asset_kinds table
INSERT INTO public.mvp_asset_kinds (name, created_at, updated_at)
SELECT kind_name,NOW(),NOW() FROM unknown_asset_kinds;