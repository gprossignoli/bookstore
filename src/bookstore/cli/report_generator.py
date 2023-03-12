import os
from datetime import datetime
from statistics import stdev


class ReportGenerator:
    def generate_report(self):
        file_path = "/home/gerardo/PycharmProjects/bookstore/src/publication_data.log"
        events_data = {}
        total_failed_publications = 0

        with open(file_path, 'r') as file:
            for line in file:
                data = line.split(",")
                event_id = data[0].replace("Event:", "")
                events_data.setdefault(event_id, {})

                timestamp_str = data[1].replace("\n", "")

                failed_publish = False
                if "failed_to_publish_at" in timestamp_str or "failed_delivery_at" in timestamp_str:
                    failed_publish = True
                    events_data[event_id]["failed_publish"] = failed_publish
                    total_failed_publications += 1

                elif "published_at" in timestamp_str:
                    timestamp_publish_str = timestamp_str.replace("published_at:", "")
                    publish_timestamp = datetime.fromisoformat(timestamp_publish_str)
                    events_data[event_id]["publish_timestamp"] = publish_timestamp

                elif "delivered_at" in timestamp_str:
                    timestamp_delivery_str = timestamp_str.replace("delivered_at:", "")
                    delivery_timestamp = datetime.fromisoformat(timestamp_delivery_str)
                    events_data[event_id]["delivery_timestamp"] = delivery_timestamp

                if failed_publish is False:
                    events_data[event_id]["failed_publish"] = failed_publish

                if events_data[event_id].get('publish_timestamp') is not None and events_data[event_id].get(
                        'delivery_timestamp') is not None:
                    throughput = events_data[event_id]['delivery_timestamp'] - events_data[event_id]['publish_timestamp']
                    events_data[event_id]['throughput'] = throughput

        print(events_data)

        file_name = datetime.now().strftime('report_%Y-%m-%d_%H_%M_%S')
        total_events = len(events_data)
        events_published = len([event for event in events_data.values() if event["failed_publish"] is False])
        events_not_published = total_events - events_published

        throughputs = [(v["throughput"].microseconds * 0.001) for v in events_data.values() if v.get("throughput") is not None]
        avg_throughput = sum(throughputs) / len(throughputs)
        stdev_throughput = stdev(throughputs)

        with open(f"/home/gerardo/PycharmProjects/bookstore/src/{file_name}", 'w+') as file:
            file.writelines([f"Events generated: {total_events}\n", f"Events published: {events_published}\n", f"Events not published: {events_not_published}\n", f"Total fails: {total_failed_publications}\n", f"Average message throughput: {'{:.2f}'.format(avg_throughput)}\n", f"Std deviaton message throughput: {'{:.2f}'.format(stdev_throughput)}\n"])


if __name__ == '__main__':
    ReportGenerator().generate_report()
