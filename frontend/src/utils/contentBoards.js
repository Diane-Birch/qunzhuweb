export const normalizeContentBoardKey = (value = "") =>
  String(value || "")
    .trim()
    .replace(/^#/, "")
    .trim();

export const sectionBoardOptions = [
  {
    value: "section-1",
    label: "\u533a\u57df 1",
    title: "\u533a\u57df 1\u5185\u5bb9\u5217\u8868",
    subtitle: "\u9996\u9875\u6838\u5fc3\u5356\u70b9\u5168\u90e8\u5386\u53f2\u5185\u5bb9",
    rule: "\u9996\u9875\u4ec5\u5c55\u793a\u6700\u65b0 1 \u6761\uff0c\u5176\u4f59\u5185\u5bb9\u6c89\u6dc0\u5230\u5217\u8868\u9875\u3002",
  },
  {
    value: "section-2",
    label: "\u533a\u57df 2",
    title: "\u533a\u57df 2\u5185\u5bb9\u5217\u8868",
    subtitle: "\u54c1\u724c\u6545\u4e8b\u5168\u90e8\u5386\u53f2\u5185\u5bb9",
    rule: "\u9996\u9875\u4ec5\u5c55\u793a\u6700\u65b0 1 \u6761\uff0c\u5176\u4f59\u5185\u5bb9\u6c89\u6dc0\u5230\u5217\u8868\u9875\u3002",
  },
  {
    value: "section-3",
    label: "\u533a\u57df 3",
    title: "\u533a\u57df 3\u5185\u5bb9\u5217\u8868",
    subtitle: "\u4ea7\u4e1a\u632f\u5174\u5168\u90e8\u5386\u53f2\u5185\u5bb9",
    rule: "\u9996\u9875\u4ec5\u5c55\u793a\u6700\u65b0 1 \u6761\uff0c\u5176\u4f59\u5185\u5bb9\u6c89\u6dc0\u5230\u5217\u8868\u9875\u3002",
  },
];

export const sectionBoardMap = Object.fromEntries(sectionBoardOptions.map((item) => [item.value, item]));

export const productArchiveConfig = {
  title: "\u4ea7\u54c1\u533a\u57df",
  subtitle: "\u5168\u90e8\u4ea7\u54c1\u5185\u5bb9",
  rule: "\u9996\u9875\u56fa\u5b9a\u5c55\u793a\u6700\u65b0 2 \u6761\uff0c\u5176\u4f59\u5185\u5bb9\u901a\u8fc7\u201c\u67e5\u770b\u66f4\u591a\u201d\u8fdb\u5165\u5217\u8868\u9875\u3002",
};

export const newsArchiveConfig = {
  title: "\u52a8\u6001\u533a\u57df",
  subtitle: "\u5168\u90e8\u4f01\u4e1a\u52a8\u6001",
  rule: "\u9996\u9875\u56fa\u5b9a\u5c55\u793a\u6700\u65b0 3 \u6761\uff0c\u5176\u4f59\u5185\u5bb9\u901a\u8fc7\u201c\u67e5\u770b\u66f4\u591a\u201d\u8fdb\u5165\u5217\u8868\u9875\u3002",
};

export const introSectionLabels = {
  product_intro: "\u4ea7\u54c1\u533a\u57df\u5bfc\u8bed",
  news_intro: "\u52a8\u6001\u533a\u57df\u5bfc\u8bed",
};

export const resolveSectionGroupKey = (section = {}) =>
  normalizeContentBoardKey(section.group_key || section.key);
