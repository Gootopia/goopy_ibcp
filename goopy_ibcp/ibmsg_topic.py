class IBTopic:
    """
    Topics are the message prefixes transmitted in network payloads.
    These enable filtering of message traffic by category or more
    ZMQ allows filtering by including the topic at the front of a message string.
    IB includes topics in JSON strings as a name/value pair "topic":"{topicvalue}"
    """

    Topic: str = "topic"
    # Marketdata arrives from IB via "smd+{conid} topics"
    MarketData: str = "smd"
    System: str = "system"
    Bulletin: str = "blt"

    @classmethod
    def process_topic(
        cls, topic: str = None, handlers: dict = None, json_msg: str = None
    ):
        """Call a handler if one has been assigned to process the topic."""
        if topic is None:
            raise ValueError("Topic string cannot be NoneType.")

        if handlers is None:
            raise ValueError("Handler dictionary cannot be NoneType.")

        if json_msg is None:
            raise ValueError("JSON message string cannot be NoneType.")

        handler_keys = handlers.keys()

        # Check handler key to see if it is a sub-string in the topic
        for handler_key in handler_keys:
            if handler_key in topic:
                # Let the handler return whatever it wants
                handler_return = handlers[handler_key](json_msg)
                return handler_return

        # Nobody handled the topic, so ignore it
        return None
