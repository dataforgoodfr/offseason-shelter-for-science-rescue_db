SELECT COUNT(*)
FROM public.mvp_downloader_library mvp
LEFT JOIN public.asset_resource ar ON mvp.resource_id = ar.resource_id
WHERE ar.resource_id IS NULL;