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

## Публикация — сделана (на 22.11.2026)
Влад 22.11.2026 выбрал «Опубликовать на vudia.site». Сделано в тот же день:
- публичный репозиторий `uvd020-tech/vudia-site` (ветка `main`), файл `CNAME` с `vudia.site`;
- GitHub Pages включены (`main`, `/`), `cname` = `vudia.site`, сборка `built`;
- Cloudflare (DNS only, TTL Auto), добавлены вручную через Playwright после входа Влада:
  четыре A у `vudia.site` — `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
  (сверены с документацией GitHub и `api.github.com/meta`) и CNAME `www` → `uvd020-tech.github.io`.
  MX и TXT (почта, SPF, DKIM, Google) не тронуты;
- проверка: `http://vudia.site/` — 200, `robots.txt`, `sitemap.xml`, `llms.txt`, `about/`,
  `apps/smart-defaults/` — 200, несуществующая страница — 404, `http://www.vudia.site/` — 301 на
  `http://vudia.site/`.

**HTTPS — включён 22.11.2026.** Сразу после записей в Cloudflare `PUT .../pages https_enforced=true`
отвечал «The certificate does not exist yet»; 30 попыток в течение ~30 минут (раз в минуту) не помогли.
Документация GitHub: DNS-проверка запускается при установке или смене домена, при зависании — убрать домен и
задать заново. Домен я задал файлом `CNAME` до появления DNS-записей. Сделано: `PUT .../pages -F cname=null`,
затем `PUT .../pages -f cname=vudia.site` (в истории два коммита от GitHub: `Delete CNAME`, `Create CNAME`;
сборка по промежуточному коммиту `Delete CNAME` дала `errored`, по `dcca093` — `built`). После этого
`https_enforced=true`, сертификат Let's Encrypt для `CN=vudia.site` до 20.02.2027. Проверка: `https://vudia.site/`
и страницы сайта — 200, `http://vudia.site/` — 301 на https, `www` — 301 на `https://vudia.site/`.
Продлевает сертификат GitHub сам (сроки продления не проверял).

**Кто имеет доступ (на 22.11.2026 21:07 UTC):** репозиторий — `uvd020-tech` (admin) и приглашённый
`Dbelokon-cpu` (Диана, логин назвал Влад; право `write`, приглашение отправлено, на момент записи не
принято). Cloudflare — только `uvd020@gmail.com` (Super admin); для правки текстов Cloudflare не нужен.

## Google Search Console (подан 22.11.2026, по часам консоли 23.11 00:5x МСК)
- Свойство типа «Domain» `vudia.site` (`sc-domain:vudia.site`, покрывает все поддомены, http и https) создано
  в аккаунте Google, открытом в окне Playwright (аватар «V», почту не видел). Владение подтверждено способом
  «Domain name provider»: в Cloudflare добавлена TXT-запись `@` = `google-site-verification=Jhsh0PZZ…`.
  **Эту запись не удалять** — иначе подтверждение слетит (так сказано в окне Google).
- Кнопку «Start verification» (выдаёт Google доступ к DNS-аккаунту Cloudflare) не нажимал — выбрал ручную TXT-запись.
- Другая TXT `google-site-verification=UFEz6l…` у `vudia.site` была раньше: токен отличается, значит выдан
  другому аккаунту Google (чьему — не знаю). Обе записи сосуществуют.
- Sitemap `https://vudia.site/sitemap.xml` подан; сразу после подачи статус был «Couldn't fetch», Live test в
  URL Inspection показал «URL is available to Google / Page can be indexed», затем статус стал «Success»,
  найдено 6 страниц. Почему был «Couldn't fetch», не установлено (документация Google называет и временные ошибки).
- В списке Sitemaps того же свойства уже были `docs`, `aging`, `crm`, `cost`.vudia.site/sitemap.xml (подача
  12–13.11.2026, Success; кто подавал — не знаю).
- «Request indexing» для страниц не нажимал.

## Bing Webmaster Tools (подан 22.11.2026 ~22:20 UTC)
- Вход: «Sign in» → Google → `uvd020@gmail.com` (выбор Влада; в браузере также есть `uvdtest@gmail.com`). Согласие
  Google — только имя, фото и почта (`openid profile email`). Аккаунт Bing Webmaster Tools у `uvd020` создан в этот
  день (при входе показан экран «Welcome», сайтов не было).
- «Import from GSC» не использовал (отдельный доступ Bing к Search Console) — сайт добавлен вручную: `https://vudia.site/`.
- Проверка владения — CNAME в Cloudflare (DNS only): `32680e9b20700835e3ebc1152d81cf77` → `verify.bing.com`.
  **Не удалять.** После «Verify» открылся дашборд сайта; явной надписи «Verified» не видел.
- Sitemap `https://vudia.site/sitemap.xml` подан, статус «Submitted — Processing», найдено 0 (на момент записи);
  Bing пишет, что данные появятся до 48 часов.
- Раньше `docs.vudia.site` подтверждали в Bing другим аккаунтом (CNAME `3cdd5c…docs.vudia.site` → `verify.bing.com`);
  чьим — не знаю. Обновить статус sitemap позже: `bing.com/webmasters/sitemaps?siteUrl=https%3A%2F%2Fvudia.site%2F`.

В кабинете Cloudflare в окне Playwright вход — кнопка «Continue as uvd020@gmail.com using Google»
на `dash.cloudflare.com/login` (пароль не нужен). Аккаунт Cloudflare: `308a8bafcbd481223525f928f1f5ffaa`.
