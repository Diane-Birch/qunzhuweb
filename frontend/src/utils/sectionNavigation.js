const SECTION_KEY_RE = /^[A-Za-z0-9_-]+$/;
const SCHEME_RE = /^[a-zA-Z][a-zA-Z\d+.-]*:/;
const SAFE_SCHEME_RE = /^(https?:|mailto:|tel:)/i;

export const normalizeSectionId = (value = "") =>
  String(value || "")
    .trim()
    .replace(/^\//, "")
    .replace(/^#/, "")
    .trim();

export const resolveSectionHash = (value = "") => {
  const raw = String(value || "").trim();
  if (!raw) {
    return "";
  }

  if (raw.startsWith("/#")) {
    const id = normalizeSectionId(raw.slice(1));
    return id ? `#${id}` : "";
  }

  if (raw.startsWith("#")) {
    const id = normalizeSectionId(raw);
    return id ? `#${id}` : "";
  }

  if (SECTION_KEY_RE.test(raw)) {
    return `#${raw}`;
  }

  return "";
};

export const resolveLinkTarget = (value = "") => {
  const raw = String(value || "").trim();
  if (!raw) {
    return { type: "none", target: "" };
  }

  const sectionHash = resolveSectionHash(raw);
  if (sectionHash) {
    return { type: "section", target: sectionHash };
  }

  if (raw.startsWith("//") || raw.startsWith("/")) {
    return { type: "url", target: raw };
  }

  if (SCHEME_RE.test(raw)) {
    return SAFE_SCHEME_RE.test(raw) ? { type: "url", target: raw } : { type: "none", target: "" };
  }

  return { type: "url", target: raw };
};

export const scrollToHash = (hash, options = {}) => {
  const id = normalizeSectionId(hash);
  if (!id || typeof window === "undefined") {
    return false;
  }

  const target = document.getElementById(id);
  if (!target) {
    return false;
  }

  const offset = options.offset ?? 96;
  const top = target.getBoundingClientRect().top + window.scrollY - offset;
  window.scrollTo({
    top: Math.max(top, 0),
    behavior: options.behavior || "smooth",
  });
  return true;
};
