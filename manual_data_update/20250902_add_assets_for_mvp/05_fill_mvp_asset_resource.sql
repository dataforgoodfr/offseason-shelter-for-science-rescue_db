CREATE TABLE IF NOT EXISTS public.mvp_asset_resource as SELECT * FROM public.asset_resource;

-- We want to keep the autoincrement value of the table
TRUNCATE TABLE public.mvp_asset_resource;

-- id column exists but should be autoincremented
ALTER TABLE public.mvp_asset_resource DROP COLUMN id;
ALTER TABLE public.mvp_asset_resource ADD COLUMN id BIGSERIAL PRIMARY KEY;

WITH mvp_unique_asset_resource AS (
    SELECT alr.resource_id, a.id FROM public.mvp_asset_less_resources alr
    INNER JOIN public.mvp_assets a ON alr.url = a.url AND alr.kind_id = a.kind_id
)

INSERT INTO public.mvp_asset_resource (asset_id, resource_id, created_at, updated_at)
SELECT id, resource_id, NOW(), NOW() FROM mvp_unique_asset_resource;