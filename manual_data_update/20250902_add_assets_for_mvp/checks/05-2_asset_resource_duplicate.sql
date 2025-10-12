SELECT asset_id, COUNT(*) FROM public.mvp_asset_resource
GROUP BY asset_id
HAVING COUNT(*) > 1;