@api_view(['GET'])
def events_with_stadiums(request):
    """
    This endpoint returns a list of all events, with the stadium where they are held.
    """
    # Get all events from the database
    events = Event.objects.all()

    # Create an empty list to store the event data
    events_data = []

    # Loop through each event and add its stadium details to the event data
    for event in events:
        # Use the tojson method to get event data and append it to events_data
        event_data = event.tojson()

        # Add the stadium info (also serialized) to the event data
        event_data['stadium'] = event.stadium.tojson() if event.stadium else None

        # Append the event data to the list
        events_data.append(event_data)

    # Return the event data as a JSON response
    return Response(events_data)


# Endpoint 2: Return events with the number of tickets sold for each event
@api_view(['GET'])
def events_with_ticket_count(request):
    """
    This endpoint returns a list of events with the number of tickets sold.
    """
    # Get all events from the database
    events = Event.objects.all()

    # Create an empty list to store the event data
    events_data = []

    # Loop through each event and count the number of tickets sold
    for event in events:
        event_data = event.tojson()  # Get event details as a dictionary
        # Count the number of tickets sold for this event
        tickets_sold = Ticket.objects.filter(event=event).count()

        # Add the ticket count to the event data
        event_data['tickets_sold'] = tickets_sold

        # Append the event data to the list
        events_data.append(event_data)

    # Return the event data with ticket counts as a JSON response
    return Response(events_data)


# Endpoint 3: A general events endpoint that can be filtered by stadium or minimum tickets
@api_view(['GET'])
def generic_events_endpoint(request):
    """
    This endpoint filters events by stadium name or the number of tickets sold (optional).
    """
    stadium_filter = request.GET.get('stadium', None)  # Get 'stadium' filter from query params
    min_tickets = request.GET.get('min_tickets', None)  # Get 'min_tickets' filter from query params

    # Get all events from the database
    events = Event.objects.all()

    # Apply filter if stadium name is provided
    if stadium_filter:
        events = events.filter(stadium__name__icontains=stadium_filter)  # Filter by stadium name

    # Apply filter if minimum ticket count is provided
    if min_tickets is not None:
        min_tickets = int(min_tickets)  # Convert the 'min_tickets' filter to an integer
        events_data = []
        for event in events:
            # Count the number of tickets sold for this event
            tickets_sold = Ticket.objects.filter(event=event).count()

            # Only include events that have sold at least 'min_tickets'
            if tickets_sold >= min_tickets:
                event_data = event.tojson()  # Get event details as a dictionary
                event_data['tickets_sold'] = tickets_sold  # Add ticket count
                events_data.append(event_data)

        # Return the filtered events with ticket counts as a JSON response
        return Response(events_data)

    # If no filters are applied, return all events
    events_data = [event.tojson() for event in events]  # Serialize all events using the tojson() method
    return Response(events_data)