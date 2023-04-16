from datetime import datetime, timedelta
from operator import itemgetter
from statistics import stdev


class ReportGenerator:
    def generate_report(self):
        file_path = "/home/gerardo/PycharmProjects/bookstore/src/publication_data.log"
        events_data = {}

        self.__obtain_events_data_from_log(events_data, file_path)

        total_events = len(events_data)
        if total_events == 0:
            self.__clean_last_experiment_from_log(log_file=file_path)

        events_published = len(
            [
                event
                for event in events_data.values()
                if event["failed_publish"] is False
            ]
        )
        events_not_published = total_events - events_published

        publication_latencies = [
            (v["publication_latency"].microseconds * 0.001)
            for v in events_data.values()
            if v.get("publication_latency") is not None
        ]
        avg_publication_latency = sum(publication_latencies) / len(publication_latencies)
        stdev_publication_latency = stdev(publication_latencies)

        throughputs = self.__calculate_total_throghput(events_data)
        avg_throughput = sum(throughputs) / len(throughputs)
        stdev_throughput = stdev(throughputs)

        file_name = datetime.now().strftime("report_%Y-%m-%d_%H_%M_%S")
        with open(
            f"/home/gerardo/PycharmProjects/bookstore/src/{file_name}.txt", "w+"
        ) as file:
            file.writelines(
                [
                    f"Events generated: {total_events}\n",
                    f"Events published: {events_published}\n",
                    f"Events not published: {events_not_published}\n",
                    f"Average publication latency: {'{:.2f}'.format(avg_publication_latency)} ms\n",
                    f"Std deviation publication latency: {'{:.2f}'.format(stdev_publication_latency)}\n",
                    f"Average total throughput: {'{:.2f}'.format(avg_throughput)} msg/sec\n",
                    f"Std deviation total throughput: {'{:.2f}'.format(stdev_throughput)}\n",
                ]
            )
        self.__clean_last_experiment_from_log(log_file=file_path)

    def __obtain_events_data_from_log(self, events_data, file_path):
        with open(file_path, "r") as file:
            for line in file:
                data = line.split(",")
                event_id = data[0].replace("Event:", "")
                events_data.setdefault(event_id, {})

                timestamp_str = data[1].replace("\n", "")

                if (
                    "failed_to_publish_at" in timestamp_str
                    or "failed_delivery_at" in timestamp_str
                ):
                    self.__mark_failed_publish(event_id, events_data)
                    continue

                else:
                    events_data[event_id]["failed_publish"] = False

                if "published_at" in timestamp_str:
                    self.__set_published_at_timestamp(
                        event_id, events_data, timestamp_str
                    )

                elif "delivered_at" in timestamp_str:
                    self.__set_delivery_timestamp(event_id, events_data, timestamp_str)

                if (
                    events_data[event_id].get("publish_timestamp") is not None
                    and events_data[event_id].get("delivery_timestamp") is not None
                ):
                    self.__set_publication_latency(event_id, events_data)

    def __mark_failed_publish(self, event_id: str, events_data: dict) -> bool:
        failed_publish = True
        events_data[event_id]["failed_publish"] = failed_publish
        return failed_publish

    def __set_published_at_timestamp(
        self, event_id: str, events_data: dict, timestamp_str: str
    ) -> None:
        timestamp_publish_str = timestamp_str.replace("published_at:", "")
        publish_timestamp = datetime.fromisoformat(timestamp_publish_str)
        events_data[event_id]["publish_timestamp"] = publish_timestamp

    def __set_delivery_timestamp(
        self, event_id: str, events_data: dict, timestamp_str: str
    ) -> None:
        timestamp_delivery_str = timestamp_str.replace("delivered_at:", "")
        delivery_timestamp = datetime.fromisoformat(timestamp_delivery_str)
        events_data[event_id]["delivery_timestamp"] = delivery_timestamp

    def __set_publication_latency(
            self, event_id: str, events_data: dict
    ) -> None:
        latency = (
            events_data[event_id]["delivery_timestamp"]
            - events_data[event_id]["publish_timestamp"]
        )
        events_data[event_id]["publication_latency"] = latency

    def __calculate_total_throghput(self, events_data):
        events_by_delivery = [
            {"event_id": k, "delivery_at": event["delivery_timestamp"]}
            for k, event in events_data.items()
            if event.get("delivery_timestamp") is not None
        ]
        events_ordered_by_delivery = sorted(
            events_by_delivery, key=itemgetter("delivery_at")
        )
        time_window_end = events_ordered_by_delivery[0]["delivery_at"] + timedelta(
            seconds=1
        )
        time_window_start = events_ordered_by_delivery[0]["delivery_at"] - timedelta(
            milliseconds=1
        )
        throughputs = [0]
        for event in events_ordered_by_delivery:
            if time_window_start <= event["delivery_at"] <= time_window_end:
                throughputs[-1] += 1

            elif event["delivery_at"] > time_window_end:
                """
                time_window_start is updated to the next message delivery,
                because any window between the last delivery and this new one without messages delivered will be 0.
                Example: last_deliveries: [00:00:00, 00:00:01] = 2 then
                next_delivery: 00:00:03 -> [00:00:01, 00:00:03) = 0
                Here we only care about throughput, so if no messages were delivered,
                we don't want to introduce a 0 in the metric.
                """
                throughputs.append(1)
                time_window_start = event["delivery_at"]
                time_window_end = time_window_start + timedelta(seconds=1)
        if sum(throughputs) != len(events_ordered_by_delivery):
            raise Exception(
                f"smth is wrong: throughputs = {throughputs}, events: {len(events_ordered_by_delivery)}"
            )
        return throughputs

    def __clean_last_experiment_from_log(self, log_file: str) -> None:
        open(log_file, "w").close()


if __name__ == "__main__":
    ReportGenerator().generate_report()
