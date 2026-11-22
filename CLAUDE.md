# Сайт вендора Vudia (vudia.site) — контекст проекта

## Что это
Статический сайт вендора Vudia со всеми приложениями: главная, страница «About» и по странице
на каждое опубликованное приложение. Цель — чтобы Vudia находили поисковики и нейросети
(идея Дианы, 22.11.2026; решение Влада «собери сайт вендора» — тот же день).
Образцы: `docs.vudia.site` (robots.txt, sitemap.xml, llms.txt, JSON-LD) и сайты Appfire и
Easy Agile (llms.txt по группам, снимок 22.11.2026 — `~/.claude/projects/D--Projects/memory/
marketplace-apps-status.md`).

## Как устроено
- `data/site.json` — единственный источник текстов: вендор, «About», приложения.
- `build.py` (только стандартная библиотека): `python build.py` пересобирает `index.html`,
  `about/`, `apps/<slug>/`, `404.html`, `robots.txt`, `sitemap.xml`, `llms.txt`.
  Сгенерированные файлы лежат в git — GitHub Pages отдаёт корень репозитория.
- `assets/style.css`, `assets/favicon.svg` — оформление; внешних шрифтов и запросов нет.
- Предпросмотр: `python -m http.server 8765` в корне репозитория, адрес `http://127.0.0.1:8765/`.

## Откуда взяты тексты (снимок 22.11.2026)
- Названия, подзаголовки и описания — публичные страницы листингов Marketplace (`<meta description>`
  и JSON-LD `SoftwareApplication`). Адрес `/rest/2/addons/<key>` отвечает 410 — не использовать.
- Разделы документации — дословно из `llms.txt` сайтов `docs`, `cost`, `aging` и из `docs/index.md`
  Smart Defaults. «Free for up to 10 users» — страницы Pricing в кабинете, все четыре.
- «About» и часы работы — вкладка Details вендора в кабинете. `info@vudia.site`, `security@vudia.site`.
- Названия на сайте = **названия листингов** (Poker ++ for Jira, Cost Tracker ++ for Jira,
  Time in Status + Gadget). Прежние названия (Planning Poker for Jira, Cost Tracker by Vudia, Time
  in Status Gadget for Jira) — в `alsoKnownAs`: так приложения названы на своих сайтах документации.

## Правила
- Тексты не придумывать: новый факт — с источником в этом файле. Цифр установок, клиентов,
  рейтингов не писать (устаревают); `AggregateRating` и `Offer` в разметку не добавлять.
- Приложение добавляется в `site.json` только после перехода листинга в PUBLIC (Spaceprint —
  пока SUBMITTED, Dealtrail CRM — SUBMITTED).
- После правки `site.json` или `build.py` — `python build.py`, коммит и пуш вместе с результатом.
- Репозиторий должен быть **публичным**: бесплатный GitHub Pages не публикует закрытые репозитории
  (`D:\Projects\Домен и сайты vudia.site.md`). Секретов здесь нет, только публичные тексты.

## Публикация — частично (на 22.11.2026)
Влад 22.11.2026 выбрал «Опубликовать на vudia.site». Сделано в тот же день (источник — вывод `gh`):
- публичный репозиторий `uvd020-tech/vudia-site` (ветка `main`);
- файл `CNAME` с `vudia.site`, коммит `a400524`;
- GitHub Pages включены (`main`, `/`), `cname` = `vudia.site`; `uvd020-tech.github.io/vudia-site/`
  отвечает 301 на `http://vudia.site/`.

**Не сделано:** записи в Cloudflare. DNS-over-HTTPS 22.11.2026: у `vudia.site` только MX, A и CNAME нет,
`www.vudia.site` не существует. Cloudflare в окне Playwright не залогинен (редирект на `/login`) —
нужен вход Влада. Нужны записи (DNS only): четыре A у `vudia.site` — `185.199.108.153`,
`185.199.109.153`, `185.199.110.153`, `185.199.111.153` и CNAME `www` → `uvd020-tech.github.io`.
После появления записей — в настройках Pages дождаться проверки домена и включить `Enforce HTTPS`.
