WITH mvp_asset_resource_mapping AS (
    SELECT mar.asset_id as mvp_asset_id, mar.resource_id as resource_id, a.id as asset_id
    FROM public.mvp_asset_resource mar
    INNER JOIN public.mvp_assets ma ON mar.asset_id = ma.id
    INNER JOIN public.assets a ON a.url = ma.url
)

INSERT INTO public.asset_resource (asset_id, resource_id)
SELECT asset_id, resource_id FROM mvp_asset_resource_mapping;