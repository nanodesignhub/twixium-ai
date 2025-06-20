// SocialSphere AI - Admin Menu Navigation Fix

/**
 * This script fixes the menu navigation in the admin dashboard
 * by properly handling click events on menu items and showing/hiding
 * the corresponding page content.
 */

document.addEventListener('DOMContentLoaded', function() {
  // Set up navigation
  setupNavigation();
  
  // Check if we're already on the admin page and apply the fix
  if (window.location.pathname.includes('/admin')) {
    console.log('Admin page detected, applying menu navigation fix');
    applyMenuFix();
  }
});

// Set up navigation
function setupNavigation() {
  const navLinks = document.querySelectorAll('.sidebar-menu a[data-page]');
  
  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      
      console.log('Menu click handler triggered for:', this.getAttribute('data-page'));
      
      // Remove active class from all links
      navLinks.forEach(l => {
        l.classList.remove('active');
      });
      
      // Add active class to clicked link
      this.classList.add('active');
      
      // Hide all pages
      document.querySelectorAll('.page').forEach(p => {
        p.style.display = 'none';
      });
      
      // Show selected page
      const pageName = this.getAttribute('data-page');
      const targetPage = document.getElementById(`${pageName}-page`);
      
      if (targetPage) {
        console.log('Showing page:', targetPage.id);
        targetPage.style.display = 'block';
        
        // Update current page
        window.currentPage = pageName;
        
        // Load page data if the function exists
        if (typeof loadPageData === 'function') {
          loadPageData(pageName);
        }
      } else {
        console.error('Target page not found:', `${pageName}-page`);
      }
    });
  });
  
  // Set up logout
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', function(e) {
      e.preventDefault();
      localStorage.removeItem('admin_token');
      window.location.href = '/login';
    });
  }
}

// Apply the menu fix immediately
function applyMenuFix() {
  const navLinks = document.querySelectorAll('.sidebar-menu a[data-page]');
  
  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      
      // Remove active class from all links
      navLinks.forEach(l => {
        l.classList.remove('active');
      });
      
      // Add active class to clicked link
      this.classList.add('active');
      
      // Hide all pages
      document.querySelectorAll('.page').forEach(p => {
        p.style.display = 'none';
      });
      
      // Show selected page
      const pageName = this.getAttribute('data-page');
      const targetPage = document.getElementById(`${pageName}-page`);
      
      if (targetPage) {
        targetPage.style.display = 'block';
        
        // Update current page
        window.currentPage = pageName;
        
        // Load page data if the function exists
        if (typeof loadPageData === 'function') {
          loadPageData(pageName);
        }
      }
    });
  });
}
