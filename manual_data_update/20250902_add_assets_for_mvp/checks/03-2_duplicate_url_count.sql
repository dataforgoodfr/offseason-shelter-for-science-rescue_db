SELECT url,COUNT(*) FROM public.mvp_asset_less_resources
GROUP BY url
HAVING COUNT(*) > 1;