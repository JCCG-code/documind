import DOMPurify from 'dompurify'
import hljs from 'highlight.js'
import MarkdownIt from 'markdown-it'

const md = new MarkdownIt({
  highlight(str: string, lang: string): string {
    if (lang && hljs.getLanguage(lang)) {
      try {
        const code = hljs.highlight(str, {
          language: lang,
          ignoreIllegals: true,
        }).value
        return `<pre class="hljs"><code>${code}</code></pre>`
      } catch {}
    }
    return `<pre class="hljs"><code>${MarkdownIt().utils.escapeHtml(str)}</code></pre>`
  },
})

export const renderMarkdown = (text: string): string =>
  DOMPurify.sanitize(md.render(text))
