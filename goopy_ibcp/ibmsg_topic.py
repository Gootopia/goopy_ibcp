class IBTopic:
    """
    Topics are the message prefixes transmitted in network payloads.
    These enable filtering of message traffic by category or more
    ZMQ allows filtering by including the topic at the front of a message string.
    IB includes topics in JSON strings as a name/value pair "topic":"{topicvalue}"
    """

    # Marketdata arrives from IB via "smd+{conid} topics"
    MarketData: str = "smd"
    System: str = "system"
    Bulletin: str = "blt"

    @classmethod
    def process_topic(cls, topic: str = None, handlers: dict = None):
        """Call a handler if one has been assigned to process the topic."""
        if topic is None:
            raise ValueError("Topic string cannot be NoneType.")

        if handlers is None:
            raise ValueError("Handler dictionary cannot be NoneType.")

        handler_keys = handlers.keys()

        # Check handler key to see if it is a sub-string in the topic
        # This lets the handler decide if it wants to fully process it or not (i.e: ticks)
        for handler_key in handler_keys:
            if handler_key in topic:
                # Let the handler return whatever it wants
                handler_return = handlers[handler_key](topic)
                return handler_return

        # If nobody handled the topic, we'll just return None to indicate that
        return None
