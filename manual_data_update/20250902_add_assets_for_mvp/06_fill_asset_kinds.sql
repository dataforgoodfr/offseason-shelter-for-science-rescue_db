INSERT INTO public.asset_kinds (name)
SELECT name FROM public.mvp_asset_kinds
WHERE name NOT IN (SELECT name FROM public.asset_kinds) ORDER BY id ASC;