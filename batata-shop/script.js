const state = {
  products: [],
  cart: [],
};

const productGrid = document.querySelector('#product-grid');
const cartElement = document.querySelector('#cart');
const overlay = document.querySelector('#overlay');
const openCartButton = document.querySelector('#open-cart');
const closeCartButton = document.querySelector('#close-cart');
const cartItems = document.querySelector('#cart-items');
const cartTotal = document.querySelector('#cart-total');
const cartCount = document.querySelector('#cart-count');
const checkoutButton = document.querySelector('#checkout');
const customerNameInput = document.querySelector('#customer-name');
const customerPhoneInput = document.querySelector('#customer-phone');
const feedbackElement = document.querySelector('#order-feedback');

const brl = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
});

function setFeedback(message, type = '') {
  feedbackElement.textContent = message;
  feedbackElement.className = `feedback ${type}`.trim();
}

function openCart() {
  cartElement.classList.add('open');
  cartElement.setAttribute('aria-hidden', 'false');
  overlay.hidden = false;
}

function closeCart() {
  cartElement.classList.remove('open');
  cartElement.setAttribute('aria-hidden', 'true');
  overlay.hidden = true;
}

function addToCart(productId) {
  const existing = state.cart.find((item) => item.id === productId);

  if (existing) {
    existing.quantity += 1;
  } else {
    const product = state.products.find((item) => item.id === productId);
    state.cart.push({ ...product, quantity: 1 });
  }

  renderCart();
}

function updateQuantity(productId, delta) {
  const item = state.cart.find((product) => product.id === productId);

  if (!item) {
    return;
  }

  item.quantity += delta;

  if (item.quantity <= 0) {
    state.cart = state.cart.filter((product) => product.id !== productId);
  }

  renderCart();
}

function getTotal() {
  return state.cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function renderProducts() {
  if (state.products.length === 0) {
    productGrid.innerHTML = '<p class="empty">Nenhum produto encontrado no banco de dados.</p>';
    return;
  }

  productGrid.innerHTML = state.products
    .map(
      (product) => `
        <article class="product-card">
          <h4>${product.name}</h4>
          <p>${product.description}</p>
          <div class="price-row">
            <span class="price">${brl.format(product.price)}</span>
            <button class="add-button" data-product-id="${product.id}">Adicionar</button>
          </div>
        </article>
      `,
    )
    .join('');

  document.querySelectorAll('.add-button').forEach((button) => {
    button.addEventListener('click', () => {
      addToCart(Number(button.dataset.productId));
    });
  });
}

function renderCart() {
  cartCount.textContent = String(state.cart.reduce((count, item) => count + item.quantity, 0));

  if (state.cart.length === 0) {
    cartItems.innerHTML = '<p class="empty">Seu carrinho está vazio.</p>';
  } else {
    cartItems.innerHTML = state.cart
      .map(
        (item) => `
          <div class="cart-item">
            <div class="cart-item-top">
              <strong>${item.name}</strong>
              <span>${brl.format(item.price * item.quantity)}</span>
            </div>
            <div class="qty-controls">
              <button data-action="decrease" data-id="${item.id}" aria-label="Diminuir">-</button>
              <span>${item.quantity}</span>
              <button data-action="increase" data-id="${item.id}" aria-label="Aumentar">+</button>
            </div>
          </div>
        `,
      )
      .join('');
  }

  cartTotal.textContent = brl.format(getTotal());

  cartItems.querySelectorAll('button[data-action]').forEach((button) => {
    button.addEventListener('click', () => {
      const id = Number(button.dataset.id);
      const delta = button.dataset.action === 'increase' ? 1 : -1;
      updateQuantity(id, delta);
    });
  });
}

async function loadProducts() {
  try {
    const response = await fetch('/api/products');

    if (!response.ok) {
      throw new Error('Falha ao carregar produtos.');
    }

    state.products = await response.json();
    renderProducts();
  } catch (error) {
    productGrid.innerHTML = `<p class="empty">${error.message}</p>`;
  }
}

async function checkout() {
  const customerName = customerNameInput.value.trim();
  const customerPhone = customerPhoneInput.value.trim();

  if (state.cart.length === 0) {
    setFeedback('Adicione pelo menos um produto no carrinho.', 'error');
    return;
  }

  if (!customerName || !customerPhone) {
    setFeedback('Preencha nome e WhatsApp para finalizar.', 'error');
    return;
  }

  checkoutButton.disabled = true;
  setFeedback('Enviando pedido...', '');

  try {
    const response = await fetch('/api/orders', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        customerName,
        customerPhone,
        items: state.cart.map((item) => ({
          productId: item.id,
          quantity: item.quantity,
        })),
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Erro ao finalizar pedido.');
    }

    setFeedback(`Pedido #${data.orderId} criado com sucesso!`, 'success');
    state.cart = [];
    renderCart();
    customerNameInput.value = '';
    customerPhoneInput.value = '';
  } catch (error) {
    setFeedback(error.message, 'error');
  } finally {
    checkoutButton.disabled = false;
  }
}

openCartButton.addEventListener('click', openCart);
closeCartButton.addEventListener('click', closeCart);
overlay.addEventListener('click', closeCart);
checkoutButton.addEventListener('click', checkout);

loadProducts();
renderCart();
