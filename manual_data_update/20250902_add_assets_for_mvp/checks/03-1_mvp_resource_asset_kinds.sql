-- Checking mvp asset less resources have all a valid asset kind
SELECT COUNT(*)
FROM public.mvp_asset_less_resources mvp
WHERE mvp.kind_id IS NULL;