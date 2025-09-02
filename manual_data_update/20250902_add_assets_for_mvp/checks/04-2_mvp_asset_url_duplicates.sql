SELECT url, COUNT(*) FROM public.mvp_assets
GROUP BY url
HAVING COUNT(*) > 1;