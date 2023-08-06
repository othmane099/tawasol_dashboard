import json

from django.shortcuts import render, redirect

from App.services import dashboard_data, save_or_update_configuration, init_configuration_form, dashboard_fake_data


def dashboard_view(request):
    """
    Generate and render the dashboard view.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered dashboard view.

    The function generates the data required for the dashboard using the 'dashboard_data()' function from the 'services' module.
    If the data is available, it renders the 'dashboard.html' template with the context containing the dashboard data and
    JSON-encoded data for the bar chart and line chart visualizations.
    If the data is not available, it redirects the user to the 'config_form' view to provide the necessary configuration data.
    """
    # Generate the dashboard data using the 'dashboard_data()' function.
    data = dashboard_data()

    if data:
        # If data is available, render the 'dashboard.html' template with the dashboard data and JSON-encoded chart data.
        return render(request, 'dashboard.html', {
            'ctx': data,
            'bar_chart': json.dumps(data['bar_chart']),
            'line_chart': json.dumps(data['line_chart'])
        })
    else:
        # If data is not available, redirect the user to the 'config_form' view to provide configuration data.
        return redirect('config_form')


def config_form_view(request):
    """
    View for rendering and handling the configuration form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered configuration form view.

    If the request method is POST, the function saves or updates the configuration based on the submitted form data
    using the 'save_or_update_configuration()' function from the 'services' module. Then, it redirects the user to the
    dashboard view ('dashboard' URL name) after successful form submission.

    If the request method is GET, the function initializes the configuration form using the 'init_configuration_form()'
    function from the 'services' module and renders the 'config_form.html' template with the form data.
    """
    if request.method == 'POST':
        # If the request method is POST, save or update the configuration based on the submitted form data.
        save_or_update_configuration(request)

        # Redirect the user to the dashboard view after successful form submission.
        return redirect('dashboard')  # Replace 'dashboard' with the URL name of your dashboard view
    else:
        # If the request method is GET, initialize the configuration form.
        form = init_configuration_form()

    # Render the 'config_form.html' template with the form data.
    return render(request, 'config_form.html', {'form': form})
