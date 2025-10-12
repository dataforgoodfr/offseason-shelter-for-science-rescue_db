CREATE TABLE IF NOT EXISTS public.mvp_assets as SELECT * FROM public.assets;

-- We want to keep the autoincrement value of the table
TRUNCATE TABLE public.mvp_assets;

-- id column exists but should be autoincremented
ALTER TABLE public.mvp_assets DROP COLUMN id;
ALTER TABLE public.mvp_assets
  ADD COLUMN id BIGSERIAL PRIMARY KEY;

-- We can group by url and kind_id because we've checked before that association is consistent
WITH mvp_unique_assets AS (
    SELECT url, kind_id FROM public.mvp_asset_less_resources
    GROUP BY url, kind_id
)

INSERT INTO public.mvp_assets (url, kind_id, created_at, updated_at)
SELECT url, kind_id, NOW(), NOW() FROM mvp_unique_assets;
