-- Update asset kinds in asset less resources temporary table
UPDATE public.mvp_asset_less_resources mvp
SET kind_id = ak.id
FROM public.mvp_asset_kinds ak
WHERE mvp.kind_name = ak.name AND mvp.kind_id IS NULL;