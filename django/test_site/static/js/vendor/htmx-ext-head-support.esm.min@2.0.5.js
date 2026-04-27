/**
 * Minified by jsDelivr using Terser v5.39.0.
 * Original file: /npm/htmx-ext-head-support@2.0.5/dist/head-support.esm.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
import htmx from "htmx.org";
!(function () {
  var e = null;
  function t(t, r) {
    if (t && t.indexOf("<head") > -1) {
      const v = document.createElement("html");
      var n = t
        .replace(/<svg(\s[^>]*>|>)([\s\S]*?)<\/svg>/gim, "")
        .match(/(<head(\s[^>]*>|>)([\s\S]*?)<\/head>)/im);
      if (n) {
        var o = [],
          d = [],
          a = [],
          h = [];
        v.innerHTML = n;
        var m = v.querySelector("head"),
          i = document.head;
        if (null == m) return;
        var u = new Map();
        for (const e of m.children) u.set(e.outerHTML, e);
        var s = e.getAttributeValue(m, "hx-head") || r;
        for (const t of i.children) {
          var l = u.has(t.outerHTML),
            c = "re-eval" === t.getAttribute("hx-head"),
            g = "true" === e.getAttributeValue(t, "hx-preserve");
          l || g
            ? c
              ? d.push(t)
              : (u.delete(t.outerHTML), a.push(t))
            : "append" === s
              ? c && (d.push(t), h.push(t))
              : !1 !==
                  e.triggerEvent(document.body, "htmx:removingHeadElement", {
                    headElement: t,
                  }) && d.push(t);
        }
        h.push(...u.values());
        for (const t of h) {
          var f = document.createRange().createContextualFragment(t.outerHTML);
          !1 !==
            e.triggerEvent(document.body, "htmx:addingHeadElement", {
              headElement: f,
            }) && (i.appendChild(f), o.push(f));
        }
        for (const t of d)
          !1 !==
            e.triggerEvent(document.body, "htmx:removingHeadElement", {
              headElement: t,
            }) && i.removeChild(t);
        e.triggerEvent(document.body, "htmx:afterHeadMerge", {
          added: o,
          kept: a,
          removed: d,
        });
      }
    }
  }
  htmx.defineExtension("head-support", {
    init: function (r) {
      ((e = r),
        htmx.on("htmx:afterSwap", function (r) {
          let n = r.detail.xhr;
          if (n) {
            var o = n.response;
            e.triggerEvent(document.body, "htmx:beforeHeadMerge", r.detail) &&
              t(o, r.detail.boosted ? "merge" : "append");
          }
        }),
        htmx.on("htmx:historyRestore", function (r) {
          e.triggerEvent(document.body, "htmx:beforeHeadMerge", r.detail) &&
            (r.detail.cacheMiss
              ? t(r.detail.serverResponse, "merge")
              : t(r.detail.item.head, "merge"));
        }),
        htmx.on("htmx:historyItemCreated", function (e) {
          e.detail.item.head = document.head.outerHTML;
        }));
    },
  });
})();
