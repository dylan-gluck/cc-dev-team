---
source: https://htmx.org/examples/
fetched: 2025-08-21
version: 2.0.6
---

# HTMX Practical Examples

## Basic Patterns

### 1. Click to Load Content
```html
<!-- Button that loads content -->
<button hx-get="/api/data" 
        hx-target="#content"
        hx-swap="innerHTML">
  Load Data
</button>
<div id="content">Content will appear here</div>

<!-- Server Response -->
<div>
  <h3>Loaded Data</h3>
  <p>This content was loaded via HTMX</p>
</div>
```

### 2. Form Submission with AJAX
```html
<!-- Form that submits without page reload -->
<form hx-post="/api/contact" 
      hx-target="#form-result"
      hx-swap="innerHTML">
  <input type="text" name="name" placeholder="Name" required>
  <input type="email" name="email" placeholder="Email" required>
  <textarea name="message" placeholder="Message" required></textarea>
  <button type="submit">Send Message</button>
</form>

<div id="form-result"></div>

<!-- Success Response -->
<div class="alert alert-success">
  <p>Thank you! Your message has been sent.</p>
</div>

<!-- Error Response (HTTP 400+) -->
<div class="alert alert-danger">
  <p>Please fix the following errors:</p>
  <ul>
    <li>Email is required</li>
    <li>Message is too short</li>
  </ul>
</div>
```

### 3. Live Search with Debouncing
```html
<!-- Search input with delayed trigger -->
<input type="text" 
       placeholder="Search products..."
       hx-get="/api/search"
       hx-target="#search-results"
       hx-trigger="keyup changed delay:300ms"
       hx-indicator="#search-loading">

<div id="search-loading" class="htmx-indicator">
  Searching...
</div>

<div id="search-results"></div>

<!-- Server Response -->
<div class="search-results">
  <div class="result-item">
    <h4>Product 1</h4>
    <p>Description of product 1</p>
  </div>
  <div class="result-item">
    <h4>Product 2</h4>
    <p>Description of product 2</p>
  </div>
</div>
```

## Advanced UI Patterns

### 4. Click to Edit (Inline Editing)
```html
<!-- Display Mode -->
<div id="contact-1" class="contact">
  <div>
    <strong>John Doe</strong><br>
    john@example.com<br>
    (555) 123-4567
  </div>
  <button hx-get="/contacts/1/edit" 
          hx-target="#contact-1"
          hx-swap="outerHTML">
    Edit
  </button>
</div>

<!-- Edit Mode (Server Response) -->
<div id="contact-1" class="contact">
  <form hx-put="/contacts/1" 
        hx-target="#contact-1"
        hx-swap="outerHTML">
    <input type="text" name="name" value="John Doe">
    <input type="email" name="email" value="john@example.com">
    <input type="tel" name="phone" value="(555) 123-4567">
    <button type="submit">Save</button>
    <button type="button" 
            hx-get="/contacts/1" 
            hx-target="#contact-1"
            hx-swap="outerHTML">
      Cancel
    </button>
  </form>
</div>
```

### 5. Modal Dialog
```html
<!-- Trigger Modal -->
<button hx-get="/modal/user-profile/123" 
        hx-target="#modal-container"
        hx-swap="innerHTML">
  View Profile
</button>

<!-- Modal Container -->
<div id="modal-container"></div>

<!-- Server Response -->
<div class="modal-backdrop" onclick="this.remove()">
  <div class="modal" onclick="event.stopPropagation()">
    <div class="modal-header">
      <h3>User Profile</h3>
      <button onclick="document.getElementById('modal-container').innerHTML = ''">
        ×
      </button>
    </div>
    <div class="modal-body">
      <h4>John Doe</h4>
      <p>Software Developer</p>
      <p>john@example.com</p>
    </div>
    <div class="modal-footer">
      <button hx-delete="/users/123" 
              hx-confirm="Are you sure?"
              hx-target="#modal-container"
              hx-swap="innerHTML">
        Delete User
      </button>
    </div>
  </div>
</div>
```

### 6. Infinite Scroll
```html
<!-- Initial Content -->
<div id="results">
  <div class="item">Item 1</div>
  <div class="item">Item 2</div>
  <div class="item">Item 3</div>
</div>

<!-- Load More Trigger -->
<div hx-get="/api/items?page=2"
     hx-target="#results"
     hx-swap="beforeend"
     hx-trigger="revealed"
     id="load-more">
  <div class="loading">Loading more items...</div>
</div>

<!-- Server Response (replaces load-more div) -->
<div class="item">Item 4</div>
<div class="item">Item 5</div>
<div class="item">Item 6</div>

<!-- New load-more div for next page -->
<div hx-get="/api/items?page=3"
     hx-target="#results"
     hx-swap="beforeend"
     hx-trigger="revealed"
     id="load-more">
  <div class="loading">Loading more items...</div>
</div>
```

### 7. Dependent Dropdowns
```html
<!-- Country Selection -->
<select name="country" 
        hx-get="/api/states" 
        hx-target="#state-container"
        hx-include="[name='country']">
  <option value="">Select Country</option>
  <option value="US">United States</option>
  <option value="CA">Canada</option>
</select>

<!-- State Container -->
<div id="state-container">
  <select name="state" disabled>
    <option>Select country first</option>
  </select>
</div>

<!-- Server Response for States -->
<select name="state" 
        hx-get="/api/cities"
        hx-target="#city-container"
        hx-include="[name='country'], [name='state']">
  <option value="">Select State</option>
  <option value="CA">California</option>
  <option value="NY">New York</option>
  <option value="TX">Texas</option>
</select>
```

## Form Patterns

### 8. Multi-Step Form
```html
<!-- Step 1 -->
<form id="multi-step-form">
  <div id="step-content">
    <h3>Step 1: Personal Information</h3>
    <input type="text" name="first_name" placeholder="First Name" required>
    <input type="text" name="last_name" placeholder="Last Name" required>
    <input type="email" name="email" placeholder="Email" required>
    
    <button type="button" 
            hx-post="/form/step2"
            hx-target="#step-content"
            hx-include="#multi-step-form"
            hx-swap="innerHTML">
      Next Step
    </button>
  </div>
</form>

<!-- Step 2 Response -->
<div>
  <h3>Step 2: Address Information</h3>
  <input type="text" name="address" placeholder="Street Address" required>
  <input type="text" name="city" placeholder="City" required>
  <input type="text" name="zip" placeholder="ZIP Code" required>
  
  <button type="button" 
          hx-post="/form/step1"
          hx-target="#step-content"
          hx-include="#multi-step-form"
          hx-swap="innerHTML">
    Previous
  </button>
  
  <button type="button" 
          hx-post="/form/submit"
          hx-target="#step-content"
          hx-include="#multi-step-form"
          hx-swap="innerHTML">
    Submit
  </button>
</div>
```

### 9. Real-time Form Validation
```html
<form hx-post="/register" hx-target="#form-messages">
  <div class="field">
    <label>Username</label>
    <input type="text" 
           name="username"
           hx-post="/validate/username"
           hx-target="#username-error"
           hx-trigger="blur"
           hx-swap="innerHTML">
    <div id="username-error"></div>
  </div>
  
  <div class="field">
    <label>Email</label>
    <input type="email" 
           name="email"
           hx-post="/validate/email"
           hx-target="#email-error"
           hx-trigger="blur"
           hx-swap="innerHTML">
    <div id="email-error"></div>
  </div>
  
  <div class="field">
    <label>Password</label>
    <input type="password" 
           name="password"
           hx-post="/validate/password"
           hx-target="#password-error"
           hx-trigger="keyup delay:500ms"
           hx-swap="innerHTML">
    <div id="password-error"></div>
  </div>
  
  <button type="submit">Register</button>
  <div id="form-messages"></div>
</form>

<!-- Validation Error Response -->
<span class="error">Username is already taken</span>

<!-- Validation Success Response -->
<span class="success">✓ Username is available</span>
```

### 10. File Upload with Progress
```html
<form hx-post="/upload" 
      hx-encoding="multipart/form-data"
      hx-target="#upload-result"
      hx-indicator="#upload-progress">
  
  <input type="file" 
         name="file" 
         accept=".pdf,.doc,.docx"
         required>
  
  <button type="submit">Upload File</button>
</form>

<div id="upload-progress" class="htmx-indicator">
  <div class="progress-bar">
    <div class="progress-fill"></div>
  </div>
  <p>Uploading...</p>
</div>

<div id="upload-result"></div>

<!-- Success Response -->
<div class="upload-success">
  <p>✓ File uploaded successfully!</p>
  <p>File: document.pdf (2.3 MB)</p>
  <a href="/downloads/document.pdf">Download</a>
</div>
```

## Dynamic Lists and Tables

### 11. Sortable Table
```html
<table>
  <thead>
    <tr>
      <th>
        <a hx-get="/users?sort=name&order=asc"
           hx-target="#user-table"
           hx-swap="outerHTML">
          Name ↑
        </a>
      </th>
      <th>
        <a hx-get="/users?sort=email&order=desc"
           hx-target="#user-table"
           hx-swap="outerHTML">
          Email ↓
        </a>
      </th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody id="user-table">
    <tr>
      <td>John Doe</td>
      <td>john@example.com</td>
      <td>
        <button hx-delete="/users/1"
                hx-target="closest tr"
                hx-swap="outerHTML"
                hx-confirm="Delete this user?">
          Delete
        </button>
      </td>
    </tr>
  </tbody>
</table>
```

### 12. Add/Remove List Items
```html
<!-- Add Item Form -->
<form hx-post="/items" 
      hx-target="#item-list"
      hx-swap="afterbegin"
      hx-on::after-request="this.reset()">
  <input type="text" name="title" placeholder="Item title" required>
  <button type="submit">Add Item</button>
</form>

<!-- Item List -->
<ul id="item-list">
  <li>
    <span>Existing Item 1</span>
    <button hx-delete="/items/1"
            hx-target="closest li"
            hx-swap="outerHTML"
            hx-confirm="Remove this item?">
      Remove
    </button>
  </li>
</ul>

<!-- New Item Response -->
<li>
  <span>New Item Title</span>
  <button hx-delete="/items/123"
          hx-target="closest li"
          hx-swap="outerHTML"
          hx-confirm="Remove this item?">
    Remove
  </button>
</li>
```

## Real-time Features

### 13. Live Updates with Polling
```html
<!-- Auto-refreshing status -->
<div hx-get="/api/status"
     hx-trigger="every 2s"
     hx-target="#status-display"
     hx-swap="innerHTML">
  <div id="status-display">
    <span class="status online">Online</span>
    <span class="last-updated">Last updated: 2 seconds ago</span>
  </div>
</div>

<!-- Live notification count -->
<div hx-get="/api/notifications/count"
     hx-trigger="every 10s"
     hx-target="#notification-badge"
     hx-swap="outerHTML">
  <span id="notification-badge" class="badge">3</span>
</div>
```

### 14. Chat Interface
```html
<!-- Chat Messages -->
<div id="chat-messages" class="chat-container">
  <div class="message">
    <strong>John:</strong> Hello everyone!
  </div>
</div>

<!-- Auto-scroll and load new messages -->
<div hx-get="/chat/messages/latest"
     hx-target="#chat-messages"
     hx-swap="beforeend"
     hx-trigger="every 1s">
</div>

<!-- Send Message Form -->
<form hx-post="/chat/send"
      hx-target="#chat-messages"
      hx-swap="beforeend"
      hx-on::after-request="this.reset()">
  <input type="text" 
         name="message" 
         placeholder="Type a message..."
         required>
  <button type="submit">Send</button>
</form>

<!-- New Message Response -->
<div class="message">
  <strong>You:</strong> This is my new message
</div>
```

## Error Handling and Loading States

### 15. Comprehensive Error Handling
```html
<button hx-get="/api/data"
        hx-target="#content"
        hx-indicator="#loading"
        hx-on::before-request="document.getElementById('error').innerHTML = ''"
        hx-on::response-error="document.getElementById('error').innerHTML = 'Failed to load data'">
  Load Data
</button>

<div id="loading" class="htmx-indicator">
  <div class="spinner"></div>
  Loading...
</div>

<div id="error" class="error-message"></div>
<div id="content"></div>

<!-- CSS for Loading States -->
<style>
.htmx-indicator {
  display: none;
}
.htmx-request .htmx-indicator {
  display: block;
}
.htmx-request .htmx-indicator {
  display: inline-block;
}
</style>
```

### 16. Retry Logic
```html
<div hx-get="/unreliable-endpoint"
     hx-target="#result"
     hx-on::response-error="
       if (event.detail.xhr.status >= 500) {
         setTimeout(() => event.target.click(), 2000);
       }
     ">
  <button>Load Data (with retry)</button>
</div>

<div id="result"></div>
```

These examples demonstrate HTMX's power in creating dynamic, interactive web applications with minimal JavaScript. Each pattern can be adapted and combined to build complex user interfaces while maintaining the simplicity and declarative nature that makes HTMX unique.