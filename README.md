# Проект за автоматско собирање и организирање на податоци од Македонската берза
Тим:
1. Анастасија Ангелова 221063
2. Софија Грковска 216103
3. Теодора Богдановска 221051

<h5>Опис на проектот</h5>
Проектот на кој што работиме има за цел да иплементира веб апликација за автоматско собирање и организирање на финансиски податоци од Македонската берза. Со употреба на Pipe-and-Filter архитектурата, системот автоматски ќе ги презема податоците од веб-страницата на Македонската берза, филтрирајќи ги и трансформирајќи ги во формат погоден за понатамошна анализа и чување во база на податоци. 
Проектот вклучува автоматизација на процесот на собирање податоци од Македонската берза за финансиски анализи, со клучни функции како што се собирање симболи на издавачи, генерација на временски интервали, паралелно собирање податоци, и зачувување на резултатите. Овој систем е дизајниран да биде ефикасен и отпорен на грешки, што овозможува брзо и прецизно собирање на податоци за финансиски анализи и извештаи.
Податоците што се собираат од Македонската берза се обемни и вклучуваат не само цени и количини на акции, туку и вредности како што се процент на промена, максимални и минимални цени, како и вкупен промет. Ова се важни метрики кои помагаат во анализа на пазарот и одредување на трендовите за одредени издавачи.

<h5>Спецификација на функциските и нефункциските барања</h5> 
Проектот за собирање и обработка на податоци од Македонската берза се состои од неколку функционални и нефункционални барања. Овој проект може да се опише преку кориснички сценариjа, со детален опис на персони и краток описен наратив.<br /> 
Функционски барања:<br />
- Автоматско преземање на податоци: Системот автоматски да ги собира кодовите на издавачите и податоците за секој издавач, притоа исклучувајќи ги обврзниците или кодовите што содржат броеви.
- Проверка на последен датум на податоци: За секој издавач, да проверува до кој датум се собрани податоците, и соодветно да ги ажурира само недостасувачките податоци.
- Трансформација на податоците: Податоците од необработен формат да се трансформираат во стандарден формат за складирање во база на податоци.
- Чување и ажурирање на податоци: Податоците треба да се зачуваат во база или структурирана датотека (CSV, JSON) и да се надополнат по потреба.
- Форматирање на датуми и цени: Системот да ги форматира датумите и цените во унифициран формат (англиска верзија и соодветни разделувачи).<br />

Нефункциски барања:<br />
- Перформанси: Податоците да се преземат и трансформираат ефикасно, оптимизирајќи го времето за целосно пополнување на базата.
- Скалабилност: Можност за проширување на системот со нови извори на податоци или нови издавачи.
- Употребливост: Системот треба да биде лесен за користење од страна на корисникот и да овозможи лесен пристап до ажурираните податоци.
- Точност на податоците: Системот да гарантира дека преземените и обработените податоци се целосно точни и конзистентни.
- Одржливост и лесно ажурирање: Кодот треба да биде лесно одржлив и да поддржува ажурирања без поголеми промени.

<h5>Кориснички сценарија:</h5>
Користник: Истражувач на пазарот<br />
Цел: Истражување на различни трендови и анализи на пазарот.<br />
Сценарио: <br />
Истражувачот на пазарот може да го користи системот за да ги анализира историските податоци од Македонската берза.
Тој се фокусира на анализи на цените, промените во обемот на трговија и колебањата на цените на акциите за различни периоди (на пример, последните 10 години).
Истражувачот ги експортира податоците во Excel или CSV формат и ги користи за напредни статистички анализи или да ги визуелизира трендовите преку графикони.
Доколку има потреба од дополнителни податоци или специфични периоди, истражувачот ги користи опциите за прецизирање на датумите за добивање на податоци за посебни периоди.
-Истражувачот добива длабок увид во движењето на акциите на македонскиот пазар и може да изготви извештаи или академски трудови за трендовите и пазарните анализи.

Користник: Претприемач во финансиски услуги<br />
Цел: Понуда на инвестициски извештаи за клиентите.<br />
Сценарио:<br />
Претприемачот го користи системот за собирање податоци за да создаде редовни извештаи за инвестициите на своите клиенти.
Тој ја започнува апликацијата која автоматски собира податоци за сите активни издавачи на Македонската берза.
Секој месец, системот генерира извештај за трендовите на пазарот, движењето на цените на акциите и другите финансиски показатели.
Претприемачот ги користи овие извештаи за да ја информира клиентелата за можностите за инвестирање.
-Претприемачот може редовно да им доставува на своите клиенти ажурирани и точни извештаи базирани на најновите податоци од берзата.
Описен наратив:
Проектот се фокусира на автоматизација на процесот на собирање на финансиски податоци од Македонската берза. Целта е да се помогне на аналитичарите и истражувачите да ги добијат потребните податоци за издавачите без да мораат рачно да ги бараат и собираат. Скриптата го автоматизира процесот на scraping, филтрирање на обврзници, собирање податоци по години и експортирање на податоци во Excel за анализа. Проектот исто така ги обезбедува нефункциските барања како што се безбедност, перформанси и леснотија на користење.
