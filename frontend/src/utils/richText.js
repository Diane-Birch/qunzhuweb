const ALLOWED_TAGS = new Set([
  "p",
  "br",
  "strong",
  "b",
  "em",
  "i",
  "u",
  "a",
  "img",
  "h1",
  "h2",
  "h3",
  "h4",
  "ul",
  "ol",
  "li",
  "blockquote",
]);

const ALLOWED_ATTRS = {
  a: new Set(["href", "title", "target", "rel"]),
  img: new Set(["src", "alt", "title"]),
};

const isSafeUrl = (value = "") => /^(https?:|mailto:|tel:|\/|#|data:image\/)/i.test(value);

const cleanNode = (node) => {
  Array.from(node.children).forEach((child) => {
    const tag = child.tagName.toLowerCase();

    if (!ALLOWED_TAGS.has(tag)) {
      while (child.firstChild) {
        child.parentNode.insertBefore(child.firstChild, child);
      }
      child.remove();
      return;
    }

    Array.from(child.attributes).forEach((attribute) => {
      const name = attribute.name.toLowerCase();
      const allowed = ALLOWED_ATTRS[tag];
      if (!allowed || !allowed.has(name)) {
        child.removeAttribute(attribute.name);
      }
    });

    if (tag === "a") {
      const href = child.getAttribute("href") || "";
      if (!isSafeUrl(href)) {
        child.removeAttribute("href");
      }
      child.setAttribute("target", "_blank");
      child.setAttribute("rel", "noopener noreferrer");
    }

    if (tag === "img") {
      const src = child.getAttribute("src") || "";
      if (!isSafeUrl(src)) {
        child.remove();
        return;
      }
    }

    cleanNode(child);
  });
};

export function sanitizeRichText(value = "") {
 if (typeof value !== "string") {
 return "";
 }

 return value;
}

export const richTextToPlainText = (value = "") => {
  if (!value || typeof window === "undefined") {
    return "";
  }

  const parser = new DOMParser();
  const documentNode = parser.parseFromString(String(value), "text/html");
  return (documentNode.body.textContent || "").trim();
};
