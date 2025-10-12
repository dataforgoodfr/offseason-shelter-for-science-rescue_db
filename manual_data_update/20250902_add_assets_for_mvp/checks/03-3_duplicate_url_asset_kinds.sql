SELECT url,kind_id,COUNT(*) FROM public.mvp_asset_less_resources
GROUP BY url,kind_id
HAVING COUNT(*) > 1;