---
source: https://htmx.org/docs/
fetched: 2025-08-21
version: 2.0.6
---

# HTMX Quick Reference

## Installation

### CDN (Recommended)
```html
<script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js"></script>
```

### NPM
```bash
npm install htmx.org@2.0.6
```

## Core Concepts

- **Hypermedia-driven**: Extend HTML's natural behavior without complex JavaScript
- **Progressive enhancement**: Works with existing HTML, graceful degradation
- **Declarative**: Define behavior through HTML attributes, not imperative code
- **Server responds with HTML**: Return HTML fragments instead of JSON

## Essential Attributes

### HTTP Request Attributes
```html
<!-- Issue HTTP requests -->
<div hx-get="/api/data">Get Data</div>
<form hx-post="/submit">Submit Form</form>
<button hx-put="/update/123">Update</button>
<button hx-delete="/item/456">Delete</button>
<button hx-patch="/partial/789">Patch</button>
```

### Core Control Attributes
```html
<!-- Target where response goes -->
<button hx-get="/data" hx-target="#result">Load</button>
<button hx-get="/data" hx-target="closest .container">Load</button>
<button hx-get="/data" hx-target="next .sibling">Load</button>

<!-- How to swap content -->
<div hx-get="/data" hx-swap="innerHTML">Replace content</div>
<div hx-get="/data" hx-swap="outerHTML">Replace element</div>
<div hx-get="/data" hx-swap="beforebegin">Insert before</div>
<div hx-get="/data" hx-swap="afterend">Insert after</div>
<div hx-get="/data" hx-swap="beforeend">Append inside</div>
<div hx-get="/data" hx-swap="afterbegin">Prepend inside</div>
<div hx-get="/data" hx-swap="delete">Remove element</div>
<div hx-get="/data" hx-swap="none">Don't swap</div>

<!-- Event triggers -->
<input hx-get="/search" hx-trigger="keyup delay:300ms">
<button hx-get="/data" hx-trigger="click once">Click once</button>
<div hx-get="/poll" hx-trigger="every 2s">Poll every 2s</div>
<div hx-get="/data" hx-trigger="revealed">Load when visible</div>
<div hx-get="/data" hx-trigger="intersect once">Load on scroll</div>
```

### Enhancement Attributes
```html
<!-- Progressive enhancement for links/forms -->
<a href="/page" hx-boost="true">Enhanced link</a>
<form action="/submit" hx-boost="true">Enhanced form</form>

<!-- Confirmation dialogs -->
<button hx-delete="/item/123" 
        hx-confirm="Are you sure you want to delete this item?">
  Delete
</button>

<!-- Loading indicators -->
<button hx-get="/slow-endpoint" 
        hx-indicator="#loading">
  Load Data
</button>
<div id="loading" class="htmx-indicator">Loading...</div>

<!-- Custom headers -->
<div hx-get="/data" 
     hx-headers='{"Authorization": "Bearer token123"}'>
  Load
</div>

<!-- Include extra values -->
<button hx-get="/search" 
        hx-include="[name='filter']">
  Search
</button>

<!-- Push URL to history -->
<a hx-get="/page1" hx-push-url="true">Page 1</a>
<a hx-get="/page2" hx-push-url="/custom-url">Page 2</a>
```

## Swap Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| `innerHTML` | Replace inner content | Default, most common |
| `outerHTML` | Replace entire element | Replacing components |
| `beforebegin` | Insert before element | Adding siblings above |
| `afterbegin` | Insert at start of element | Prepending to lists |
| `beforeend` | Insert at end of element | Appending to lists |
| `afterend` | Insert after element | Adding siblings below |
| `delete` | Remove target element | Removing items |
| `none` | Don't swap anything | Status updates only |

## Event Triggers

### Standard Events
```html
<!-- Default events by element type -->
<input hx-get="/search">                    <!-- input, change -->
<textarea hx-post="/save">                  <!-- input, change -->
<select hx-get="/filter">                   <!-- change -->
<button hx-post="/action">                  <!-- click -->
<form hx-post="/submit">                    <!-- submit -->

<!-- Explicit events -->
<div hx-get="/data" hx-trigger="click">Click me</div>
<div hx-get="/data" hx-trigger="mouseenter">Hover</div>
<div hx-get="/data" hx-trigger="focus">Focus</div>
<div hx-get="/data" hx-trigger="blur">Blur</div>
<div hx-get="/data" hx-trigger="keyup">Key up</div>
```

### Event Modifiers
```html
<!-- Timing modifiers -->
<input hx-get="/search" hx-trigger="keyup delay:300ms">
<div hx-get="/data" hx-trigger="click once">
<div hx-get="/refresh" hx-trigger="every 5s">

<!-- Condition modifiers -->
<input hx-get="/search" hx-trigger="keyup[target.value.length > 2]">
<button hx-post="/save" hx-trigger="click[event.ctrlKey]">

<!-- Special triggers -->
<div hx-get="/data" hx-trigger="load">         <!-- On page load -->
<div hx-get="/data" hx-trigger="revealed">     <!-- When element visible -->
<div hx-get="/data" hx-trigger="intersect">    <!-- Intersection observer -->
```

## HTTP Headers

### Request Headers (Sent by HTMX)
```
HX-Request: true                    // Always sent
HX-Trigger: element-id             // ID of triggered element
HX-Trigger-Name: button-name       // Name of triggered element
HX-Target: target-id               // ID of target element
HX-Current-URL: /current/path      // Current page URL
HX-Boosted: true                   // If request is boosted
HX-Prompt: user-input              // User input from hx-prompt
```

### Response Headers (Server to HTMX)
```
HX-Location: /new/page             // Client-side redirect
HX-Push-Url: /new/url              // Update browser URL
HX-Redirect: /login                // Full page redirect
HX-Refresh: true                   // Refresh the page
HX-Replace-Url: /current           // Replace current URL
HX-Reswap: innerHTML               // Override swap method
HX-Retarget: #new-target           // Override target
HX-Reselect: .content              // Select part of response
HX-Trigger: {"event": "data"}      // Trigger client events
HX-Trigger-After-Settle: {...}     // Trigger after settle
HX-Trigger-After-Swap: {...}       // Trigger after swap
```

## JavaScript API

### Configuration
```javascript
// Configure HTMX behavior
htmx.config.historyEnabled = true;
htmx.config.defaultSwapStyle = 'innerHTML';
htmx.config.defaultSwapDelay = 0;
htmx.config.defaultSettleDelay = 20;
htmx.config.includeIndicatorStyles = true;
```

### Methods
```javascript
// Trigger requests programmatically
htmx.ajax('GET', '/api/data', '#target');
htmx.ajax('POST', '/api/save', {
  target: '#result',
  swap: 'innerHTML',
  values: {name: 'John', email: 'john@example.com'}
});

// Find and process elements
htmx.process(document.body);        // Process HTMX attributes
htmx.find('#my-element');           // Find element with HTMX
htmx.findAll('.htmx-elements');     // Find all HTMX elements

// Trigger events
htmx.trigger('#element', 'myEvent', {detail: 'data'});

// Remove HTMX from element
htmx.remove('#element');
```

### Events
```javascript
// Request lifecycle events
document.addEventListener('htmx:beforeRequest', function(evt) {
  console.log('About to make request', evt.detail);
});

document.addEventListener('htmx:afterRequest', function(evt) {
  console.log('Request completed', evt.detail);
});

document.addEventListener('htmx:beforeSwap', function(evt) {
  console.log('About to swap content', evt.detail);
});

document.addEventListener('htmx:afterSwap', function(evt) {
  console.log('Content swapped', evt.detail);
});

// Error handling
document.addEventListener('htmx:responseError', function(evt) {
  console.error('Request failed', evt.detail);
});

document.addEventListener('htmx:sendError', function(evt) {
  console.error('Network error', evt.detail);
});
```

## Common Patterns

### Active Search
```html
<input type="text" 
       placeholder="Search..."
       hx-get="/search"
       hx-target="#search-results"
       hx-trigger="keyup changed delay:300ms">
<div id="search-results"></div>
```

### Infinite Scroll
```html
<div id="content">
  <!-- Initial content -->
</div>
<div hx-get="/api/more?page=2"
     hx-target="#content"
     hx-swap="beforeend"
     hx-trigger="revealed">
  Loading more...
</div>
```

### Click to Edit
```html
<div id="contact-1">
  <span>John Doe</span>
  <button hx-get="/edit/1" 
          hx-target="#contact-1">
    Edit
  </button>
</div>

<!-- Server returns edit form that replaces the div -->
```

### Form Validation
```html
<form hx-post="/validate" hx-target="#errors">
  <input name="email" 
         hx-post="/validate-email"
         hx-target="#email-error"
         hx-trigger="blur">
  <div id="email-error"></div>
  
  <div id="errors"></div>
  <button type="submit">Submit</button>
</form>
```

### Modal Dialog
```html
<button hx-get="/modal-content" 
        hx-target="#modal" 
        hx-swap="innerHTML"
        onclick="document.getElementById('modal').showModal()">
  Open Modal
</button>

<dialog id="modal">
  <!-- Modal content loaded here -->
</dialog>
```

### File Upload with Progress
```html
<form hx-post="/upload" 
      hx-encoding="multipart/form-data"
      hx-target="#upload-result"
      hx-indicator="#upload-progress">
  <input type="file" name="file">
  <button type="submit">Upload</button>
</form>

<div id="upload-progress" class="htmx-indicator">
  Uploading...
</div>
<div id="upload-result"></div>
```

## Troubleshooting

### Common Issues

1. **Requests not firing**: Check that HTMX script is loaded
2. **Content not updating**: Verify target selector exists
3. **Forms not submitting**: Ensure form has proper action attribute when using `hx-boost`
4. **History not working**: Check `htmx.config.historyEnabled = true`
5. **Indicators not showing**: Include HTMX CSS or set `includeIndicatorStyles: true`

### Debug Tools
```javascript
// Enable logging
htmx.logAll();

// Inspect element's HTMX data
htmx.find('#element');

// Check if element is processed
element.hasAttribute('hx-get');
```

### CSS for Indicators
```css
.htmx-indicator {
  display: none;
}

.htmx-request .htmx-indicator {
  display: block;
}

.htmx-request.htmx-indicator {
  display: block;
}
```

## Extensions

HTMX supports extensions for additional functionality:
- WebSocket support
- Server-Sent Events (SSE)  
- JSON encoding
- Client-side templates
- Preload
- Loading states

Load extensions via CDN or npm and enable with `hx-ext` attribute:
```html
<div hx-ext="ws" ws-connect="/chatroom">
  WebSocket content
</div>
```