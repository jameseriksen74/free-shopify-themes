/* Zapline theme by Pretty Things Online (prettythingsonline.com). MIT licensed. */
(function () {
  'use strict';

  // Close other dropdowns and panels when one opens or on outside click.
  document.addEventListener('click', function (event) {
    document.querySelectorAll('details[open][data-dropdown], details[open][data-search], details[open][data-mobile-nav]').forEach(function (el) {
      if (!el.contains(event.target)) el.removeAttribute('open');
    });
  });
  document.addEventListener('keyup', function (event) {
    if (event.key !== 'Escape') return;
    document.querySelectorAll('details[open]').forEach(function (el) {
      el.removeAttribute('open');
      var summary = el.querySelector('summary');
      if (summary) summary.focus();
    });
  });

  // Focus the search input when the panel opens.
  var search = document.querySelector('[data-search]');
  if (search) {
    search.addEventListener('toggle', function () {
      if (search.open) {
        var input = search.querySelector('input[type="search"]');
        if (input) input.focus();
      }
    });
  }

  // Predictive search.
  var predictiveInput = document.querySelector('[data-predictive-input]');
  var predictiveResults = document.querySelector('[data-predictive-results]');
  if (predictiveInput && predictiveResults && window.Shopify && window.Shopify.routes) {
    var timer;
    predictiveInput.addEventListener('input', function () {
      clearTimeout(timer);
      var q = predictiveInput.value.trim();
      if (q.length < 2) { predictiveResults.innerHTML = ''; return; }
      timer = setTimeout(function () {
        fetch(window.Shopify.routes.root + 'search/suggest?q=' + encodeURIComponent(q) + '&resources[type]=product&resources[limit]=5&section_id=predictive-search')
          .then(function (r) { return r.text(); })
          .then(function (html) {
            var doc = new DOMParser().parseFromString(html, 'text/html');
            var found = doc.querySelector('.predictive');
            predictiveResults.innerHTML = found ? found.outerHTML : '';
          })
          .catch(function () { predictiveResults.innerHTML = ''; });
      }, 250);
    });
  }

  // Auto-submit sorting.
  document.querySelectorAll('[data-auto-submit]').forEach(function (el) {
    el.addEventListener('change', function () { el.form.submit(); });
  });

  // Product page: gallery thumbnails and variant picking.
  document.querySelectorAll('[data-product]').forEach(function (root) {
    var mainImage = root.querySelector('[data-main-image]');
    function showImage(src) {
      if (!mainImage || !src) return;
      mainImage.removeAttribute('srcset');
      mainImage.src = src;
    }
    root.querySelectorAll('[data-thumb]').forEach(function (thumb) {
      thumb.addEventListener('click', function () {
        root.querySelectorAll('[data-thumb]').forEach(function (t) { t.removeAttribute('aria-current'); });
        thumb.setAttribute('aria-current', 'true');
        showImage(thumb.getAttribute('data-src'));
      });
    });

    var form = root.querySelector('[data-product-form]');
    var variantsEl = root.querySelector('[data-variants]');
    if (!form || !variantsEl) return;
    var variants = JSON.parse(variantsEl.textContent);
    var select = form.querySelector('[data-variant-select]');
    var addButton = form.querySelector('[data-add-button]');
    var strings = window.themeStrings || {};

    form.addEventListener('change', function (event) {
      if (!event.target.matches('[data-option-index]')) return;
      var selected = [];
      form.querySelectorAll('fieldset.option').forEach(function (fs) {
        var checked = fs.querySelector('input:checked');
        selected.push(checked ? checked.value : null);
      });
      var variant = variants.find(function (v) {
        return v.options.every(function (opt, i) { return opt === selected[i]; });
      });
      if (!variant) {
        addButton.disabled = true;
        addButton.textContent = strings.unavailable || 'Unavailable';
        return;
      }
      select.value = variant.id;
      addButton.disabled = !variant.available;
      addButton.textContent = variant.available ? strings.addToCart : strings.soldOut;
      var url = new URL(window.location.href);
      url.searchParams.set('variant', variant.id);
      window.history.replaceState({}, '', url.toString());
      if (variant.featured_image) {
        showImage(variant.featured_image.src);
      }
      // Refresh price and pickup from the server-rendered section.
      fetch(url.pathname + '?variant=' + variant.id + '&section_id=' + root.getAttribute('data-section'))
        .then(function (r) { return r.text(); })
        .then(function (html) {
          var doc = new DOMParser().parseFromString(html, 'text/html');
          ['[data-price]', '[data-pickup]'].forEach(function (sel) {
            var fresh = doc.querySelector(sel);
            var current = root.querySelector(sel);
            if (fresh && current) current.innerHTML = fresh.innerHTML;
          });
        })
        .catch(function () {});
    });
  });

  // Related products.
  document.querySelectorAll('[data-recommendations]').forEach(function (el) {
    fetch(el.getAttribute('data-url'))
      .then(function (r) { return r.text(); })
      .then(function (html) {
        var doc = new DOMParser().parseFromString(html, 'text/html');
        var section = doc.querySelector('.shopify-section');
        if (section && section.innerHTML.trim().length) el.innerHTML = section.innerHTML;
      })
      .catch(function () {});
  });

  // Gentle reveal on scroll.
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px' });
    document.querySelectorAll('.product-card, .collection-card, .quote, .image-text__media, .article-card').forEach(function (el) {
      el.classList.add('reveal');
      observer.observe(el);
    });
  }
})();
