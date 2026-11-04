# Design decisions — and why

Draft 1, 3 November 2026. Every choice here is open to change; the reason is what to argue with.

## Structure

1. **Six plain HTML files, no framework or build step.** You can read and edit every file directly, GitHub Pages serves them as they are, and nothing breaks when a tool updates. Cost: the nav and footer are copied on all six pages, so a change there means six edits. If that gets annoying, GitHub Pages' built-in Jekyll can share one nav file — a later upgrade, not needed now.
2. **One stylesheet for all pages.** Colours and fonts are defined once at the top, so the whole site stays in one colour scheme even though each page looks different.
3. **Each page gets a class on `<body>` (`page-dance` etc.).** That is how one stylesheet gives each page its own layout and mood without separate CSS files.
4. **`.nojekyll` file.** Stops GitHub running Jekyll on the folder, which would hide any file or folder starting with `_` and slow every publish.

## Colours

5. **Two primary colours: deep teal `#0F5C5C` and living coral `#FF6F61`, plus black, white and greys.** Chosen 3 Nov 2026, replacing blue and amber. Teal is in the blue family, so it keeps the trustworthy feel for research and industry, and it reads as "science and biology" more than corporate blue does. Coral is warm and lively for dance and cooking. They sit opposite each other on the colour wheel, so each makes the other stand out. Coral is too light for small text on white, so text uses the darker coral `#C44536` (`--b-dark`) and coral buttons use dark text.
6. **Changing them:** edit `--a` (teal) and `--b` (coral) at the top of `style.css`. The `-dark` and `-soft` lines are darker and lighter shades of each; change them together.

## Each page's flair

7. **Home — split hero with portrait, then five photo tiles.** Research and industry tiles are larger and first, because CV readers land here and should see the professional doors first. The amber block behind the portrait borrows the bold, blocky look of the construction-company template.
8. **"Right now" band on home.** A site with a recent date looks alive; an old one looks abandoned. This is the one section to update every month or two.
9. **Research — clean, two columns, sticky side menu.** Academic readers scan for specific things (degree, supervisor, thesis). A side menu lets them jump straight there. Other projects are collapsible notes, as you asked — hidden until clicked, so the page stays short.
10. **Industry — timeline of roles.** Recruiters read experience in date order; a timeline shows that at a glance. "Kinds of work" cards come first because they answer "what can this person do" before "where have they been".
11. **Programming — dark header with a blinking cursor, progress bars for the game.** The bars reuse your own progress-check numbers (31 Oct 2026), so the page shows a real project in motion rather than a claim. Update them after each progress check.
12. **XY and Ising GIFs live on the programming page, with a one-line link from research.** They are strong evidence that you can turn complex physics into working code, which is a programming point first. On the research page they would compete with your actual thesis question. The link keeps them one click away for academics. Check with your supervisors if they are thesis figures.
13. **Dance — black "stage" page with a full-screen photo and amber highlights.** It is the most visual page, in the spirit of the videographer template: big media, little text. Reel tiles are 9:16 to match Instagram reels.
14. **Reels are links with cover images, not live embeds, by default.** Embeds load slowly, vary in size and depend on Instagram's script. Links look exactly as designed. The README explains how to switch to real embeds.
15. **Cooking — menu card plus polaroid gallery plus recipe book.** You asked for menu, recipe book, or both. The menu is the "front of house" summary; each dish links to its full recipe below, which opens automatically. Serif and handwriting fonts make it feel casual and warm; the colours stay the same.

## Content and placeholders

16. **Facts I already knew are filled in** (degree names, universities, years, thesis title, supervisors, group and show names you listed). Everything else is a `TODO`, so nothing is invented.
17. **Placeholder images have their final names and sizes written on them.** You replace the file and the page updates — no code edits for photos.
18. **Yellow dashed boxes on unfilled text.** You can see at a glance what is left, and visitors will never see them once `class="ph"` is removed.

## Not done yet, on purpose

- No dark mode — not asked for, and the dance page is already dark.
- No contact form — GitHub Pages cannot run server code. An email link does the job; Formspree can add a form later.
- No favicon (the little tab icon) — add one once you have a logo or initials design.
- The example templates you sent block automated access, so draft 1 is based on what those template styles generally look like. Point out anything that is off.
