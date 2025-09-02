SELECT COUNT(*)
FROM public.mvp_asset_resource mar
INNER JOIN public.mvp_assets ma ON mar.asset_id = ma.id
INNER JOIN public.assets a ON a.url = ma.url;