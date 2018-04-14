/* Project specific Javascript goes here. */

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
$('.form-group').removeClass('row');

// Requires <script src="https://js.stripe.com/v3/"></script> to be included in your page

const loadStripeElements = () => {
  const form = document.querySelector('form[data-stripe-key]');
  if (form === null) {
    return;
  }
  const key = form.getAttribute('data-stripe-key');
  if (key) {
    if (Stripe === undefined) {
      throw('pinax-stripe integration requires that https://js.stripe.com/v3/ is loaded in a script tag in your page.');
    }
    const stripe = Stripe(key);
    const elements = stripe.elements();
    const card = elements.create('card');
    const errorElement = document.getElementById(form.getAttribute('data-card-errors-id'));
    card.mount(`#${form.getAttribute('data-card-mount-id')}`);

    card.addEventListener('change', (event) => {
      if (event.error) {
        errorElement.textContent = event.error.message;
      } else {
        errorElement.textContent = '';
      }
    });

    // Handle form submission
    form.addEventListener('submit', (event) => {
      event.preventDefault();

      stripe.createToken(card).then((result) => {
        if (result.error) {
          // Inform the user if there was an error
          errorElement.textContent = result.error.message;
        } else {
          const tokenInput = document.createElement('input');
          tokenInput.setAttribute('type', 'hidden');
          tokenInput.setAttribute('name', 'stripeToken');
          tokenInput.setAttribute('value', result.token.id);
          form.appendChild(tokenInput);
          form.submit();
        }
      });
    });
  }
};

loadStripeElements();
