SELECT COUNT(*)
FROM public.mvp_downloader_library mvp
INNER JOIN public.resources r ON mvp.resource_id = r.id
LEFT JOIN public.asset_resource ar ON mvp.resource_id = ar.resource_id
LEFT JOIN public.asset_kinds ak ON r.resource_type = ak.name
WHERE ar.resource_id IS NULL;