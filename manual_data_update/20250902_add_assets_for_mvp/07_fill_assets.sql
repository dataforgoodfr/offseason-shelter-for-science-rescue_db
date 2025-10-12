WITH mvp_asset_mapping AS (
    SELECT ma.url, mak.id as mvp_kind_id, ak.id as kind_id
    FROM public.mvp_assets ma
    INNER JOIN public.mvp_asset_kinds mak ON mak.id = ma.kind_id
    INNER JOIN public.asset_kinds ak ON ak.name = mak.name
)

INSERT INTO public.assets (url, kind_id)
SELECT url, kind_id FROM mvp_asset_mapping;