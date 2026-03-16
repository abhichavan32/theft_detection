// ========================================
// Electricity Theft Detection System
// Advanced Animations & Interactions
// ========================================

document.addEventListener('DOMContentLoaded', function() {
  
  // ===== SMOOTH SCROLL BEHAVIOR =====
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // ===== OBSERVE ELEMENTS FOR ANIMATION =====
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animation = entry.target.dataset.animation || 'slideUp 0.6s ease-out forwards';
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Observe all animated elements
  document.querySelectorAll('[data-animation]').forEach(el => {
    observer.observe(el);
  });

  // ===== NAVBAR LINK ACTIVE STATE =====
  function updateActiveNavLink() {
    const links = document.querySelectorAll('nav a');
    links.forEach(link => {
      if (link.href === window.location.href) {
        link.style.background = 'var(--secondary)';
        link.style.color = 'white';
      } else {
        link.style.background = '';
        link.style.color = '';
      }
    });
  }
  updateActiveNavLink();

  // ===== FORM INPUT FOCUS ANIMATION =====
  const inputs = document.querySelectorAll('input, select, textarea');
  inputs.forEach(input => {
    input.addEventListener('focus', function() {
      this.parentElement.style.transform = 'translateY(-2px)';
    });
    
    input.addEventListener('blur', function() {
      this.parentElement.style.transform = 'translateY(0)';
    });
  });

  // ===== BUTTON RIPPLE EFFECT =====
  const buttons = document.querySelectorAll('button');
  buttons.forEach(button => {
    button.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;
      
      ripple.style.width = ripple.style.height = size + 'px';
      ripple.style.left = x + 'px';
      ripple.style.top = y + 'px';
      ripple.classList.add('ripple');
      
      this.appendChild(ripple);
      
      setTimeout(() => ripple.remove(), 600);
    });
  });

  // ===== TABLE ROW HOVER EFFECTS =====
  const tableRows = document.querySelectorAll('tbody tr');
  tableRows.forEach(row => {
    row.addEventListener('mouseenter', function() {
      this.style.background = 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)';
    });
    
    row.addEventListener('mouseleave', function() {
      this.style.background = '';
    });
  });

  // ===== STAT CARDS COUNTER ANIMATION =====
  function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const range = target - start;
    const increment = range / (duration / 16);
    let current = start;

    const counter = setInterval(() => {
      current += increment;
      if (current >= target) {
        element.textContent = target;
        clearInterval(counter);
      } else {
        element.textContent = Math.floor(current);
      }
    }, 16);
  }

  // Observe stat cards
  const statValues = document.querySelectorAll('.stat-card .value, .stat-box .value');
  statValues.forEach(card => {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const text = entry.target.textContent;
          const number = parseInt(text);
          if (!isNaN(number) && number > 0) {
            animateCounter(entry.target, number);
          }
          observer.unobserve(entry.target);
        }
      });
    });
    observer.observe(card);
  });

  // ===== BADGE ANIMATION =====
  const badges = document.querySelectorAll('.badge');
  badges.forEach(badge => {
    badge.addEventListener('mouseenter', function() {
      this.style.transform = 'scale(1.08) rotateZ(2deg)';
    });
    
    badge.addEventListener('mouseleave', function() {
      this.style.transform = 'scale(1) rotateZ(0deg)';
    });
  });

  // ===== SCROLL PROGRESS INDICATOR =====
  function updateScrollProgress() {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;
    
    // Create progress bar if it doesn't exist
    if (!document.querySelector('.scroll-progress')) {
      const progressBar = document.createElement('div');
      progressBar.className = 'scroll-progress';
      progressBar.style.position = 'fixed';
      progressBar.style.top = '0';
      progressBar.style.left = '0';
      progressBar.style.height = '3px';
      progressBar.style.background = 'linear-gradient(90deg, #10b981 0%, #059669 100%)';
      progressBar.style.zIndex = '9999';
      progressBar.style.transition = 'width 0.1s ease';
      document.body.appendChild(progressBar);
    }
    
    document.querySelector('.scroll-progress').style.width = scrollPercent + '%';
  }
  
  window.addEventListener('scroll', updateScrollProgress);

  // ===== LOADING SPINNER ANIMATION =====
  if (document.querySelector('.loading')) {
    const loading = document.querySelector('.loading');
    loading.addEventListener('DOMNodeInserted', function() {
      if (this.classList.contains('show')) {
        this.innerHTML = '<span class="spinner"></span> Processing...';
      }
    });
  }

  // ===== TOAST NOTIFICATIONS =====
  window.showToast = function(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = type;
    toast.textContent = message;
    toast.style.position = 'fixed';
    toast.style.bottom = '20px';
    toast.style.right = '20px';
    toast.style.padding = '1rem 1.5rem';
    toast.style.borderRadius = '8px';
    toast.style.color = 'white';
    toast.style.zIndex = '10000';
    toast.style.animation = 'slideInRight 0.3s ease-out';
    
    if (type === 'success') {
      toast.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
    } else if (type === 'error') {
      toast.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
    } else if (type === 'warning') {
      toast.style.background = 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)';
    } else {
      toast.style.background = 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)';
    }
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
      toast.style.animation = 'slideInRight 0.3s ease-out reverse';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  };

  // ===== DARK MODE TOGGLE (Optional) =====
  const darkModeToggle = document.querySelector('[data-dark-mode]');
  if (darkModeToggle) {
    darkModeToggle.addEventListener('click', function() {
      document.body.classList.toggle('dark-mode');
      localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
    });

    // Check saved preference
    if (localStorage.getItem('darkMode') === 'true') {
      document.body.classList.add('dark-mode');
    }
  }

  // ===== LAZY LOAD IMAGES =====
  if ('IntersectionObserver' in window) {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.style.animation = 'fadeIn 0.3s ease-out';
          imageObserver.unobserve(img);
        }
      });
    });
    images.forEach(img => imageObserver.observe(img));
  }

});

// ===== CSS FOR RIPPLE EFFECT =====
const style = document.createElement('style');
style.textContent = `
  button {
    position: relative;
    overflow: hidden;
  }

  .ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.5);
    transform: scale(0);
    animation: rippleAnimation 0.6s ease-out;
    pointer-events: none;
  }

  @keyframes rippleAnimation {
    to {
      transform: scale(4);
      opacity: 0;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .ripple {
      animation: none;
    }
  }
`;
document.head.appendChild(style);
