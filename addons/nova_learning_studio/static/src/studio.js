/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

// The fullscreen player inserts articles after navigation. One delegated handler
// also serves the standard lesson page without retaining a previous lesson.
document.addEventListener("change", (event) => {
    if (!event.target.matches(".nova-calculator select")) {
        return;
    }
    const advance = 2600 * Number(event.target.value) / 100;
    const balance = advance - 2100;
    const amount = new Intl.NumberFormat("ar").format(Math.abs(balance));
    const message = balance < 0 ? `فجوة قدرها ${amount} وحدة.` : `فائض قدره ${amount} وحدة.`;
    event.target.closest(".nova-calculator").querySelector("output").textContent = message;
});

// Lesson sections. Every Nova article uses the same <h3> headings. On the page
// each heading and its paragraphs become a styled block, and the model answers
// are folded so learners attempt the task first. This is presentation only:
// the widget restores the original markup before the website editor starts,
// so the wrappers can never be saved into the lesson. Without JavaScript the
// article stays fully readable.
const BLOCKS = {
    "الحالة": "case",
    "طريقة الحل": "method",
    "تطبيق موجّه": "task",
    "خطأ شائع": "pitfall",
    "خلاصة الدرس": "takeaway",
    "اختبر فهمك": "check",
};
const REVEALS = {
    "قارن طريقتك": "قارن طريقتك — اكشفها بعد إنجاز المهمة",
    "إجابة مقترحة": "الإجابة المقترحة — اكشفها بعد كتابة إجابتك",
};
const ARTICLES = 'div[dir="rtl"][lang="ar"]';

function enhance(article) {
    if (article.dataset.novaSections || !article.querySelector(":scope > h3")) {
        return;
    }
    article.dataset.novaSections = "1";
    for (const heading of [...article.querySelectorAll(":scope > h3")]) {
        const title = heading.textContent.trim();
        const kind = BLOCKS[title];
        const reveal = REVEALS[title];
        if (!kind && !reveal) {
            continue;
        }
        const body = [];
        for (let next = heading.nextElementSibling; next && next.tagName !== "H3"; next = next.nextElementSibling) {
            body.push(next);
        }
        if (reveal) {
            const details = document.createElement("details");
            details.className = "nova-reveal";
            const summary = document.createElement("summary");
            summary.textContent = reveal;
            heading.replaceWith(details);
            // Keep the heading (hidden) so restore() can put it back unchanged.
            heading.hidden = true;
            details.append(summary, heading, ...body);
        } else {
            const section = document.createElement("section");
            section.className = `nova-block nova-block--${kind}`;
            heading.before(section);
            section.append(heading, ...body);
        }
    }
}

function restore(article) {
    if (!article.dataset.novaSections) {
        return;
    }
    for (const wrapper of article.querySelectorAll(":scope > .nova-block, :scope > .nova-reveal")) {
        wrapper.querySelector(":scope > summary")?.remove();
        const heading = wrapper.querySelector(":scope > h3");
        if (heading) {
            heading.hidden = false;
        }
        wrapper.replaceWith(...wrapper.childNodes);
    }
    delete article.dataset.novaSections;
}

publicWidget.registry.NovaLessonSections = publicWidget.Widget.extend({
    selector: ".o_wslides_lesson_content_type",
    disabledInEditableMode: true,

    start() {
        this.el.querySelectorAll(ARTICLES).forEach(enhance);
        return this._super(...arguments);
    },
    destroy() {
        this.el.querySelectorAll(ARTICLES).forEach(restore);
        this._super(...arguments);
    },
});

// Fullscreen player: articles arrive by RPC and are never editable there.
function watchFullscreen() {
    const player = document.querySelector(".o_wslides_fs_main");
    if (!player) {
        return;
    }
    const scan = () => player.querySelectorAll(ARTICLES).forEach(enhance);
    scan();
    new MutationObserver(scan).observe(player, { childList: true, subtree: true });
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", watchFullscreen);
} else {
    watchFullscreen();
}
