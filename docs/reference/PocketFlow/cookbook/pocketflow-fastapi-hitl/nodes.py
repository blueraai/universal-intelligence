from pocketflow import Node, AsyncNode
from utils.process_task import process_task

class ProcessNode(Node):
    def prep(self, shared):
        task_input = shared.get("task_input", "No input")
        print("ProcessNode Prep")
        return task_input

    def exec(self, prep_res):
        return process_task(prep_res)

    def post(self, shared, prep_res, exec_res):
        shared["processed_output"] = exec_res
        print("ProcessNode Post: Output stored.")
        return "default" # Go to ReviewNode

class ReviewNode(AsyncNode):
    async def prep_async(self, shared):
        review_event = shared.get("review_event")
        queue = shared.get("sse_queue") # Expect queue in shared
        processed_output = shared.get("processed_output", "N/A")

        if not review_event or not queue:
            print("ERROR: ReviewNode Prep - Missing review_event or sse_queue in shared store!")
            return None # Signal failure

        # Push status update to SSE queue
        status_update = {
            "status": "waiting_for_review",
            "output_to_review": processed_output
        }
        await queue.put(status_update)
        print("ReviewNode Prep: Put 'waiting_for_review' on SSE queue.")

        return review_event # Return event for exec_async

    async def exec_async(self, prep_res):
        review_event = prep_res
        if not review_event:
            print("ReviewNode Exec: Skipping wait (no event from prep).")
            return
        print("ReviewNode Exec: Waiting on review_event...")
        await review_event.wait()
        print("ReviewNode Exec: review_event set.")

    async def post_async(self, shared, prep_res, exec_res):
        feedback = shared.get("feedback")
        print(f"ReviewNode Post: Processing feedback '{feedback}'")

        # Clear the event for potential loops
        review_event = shared.get("review_event")
        if review_event:
            review_event.clear()
        shared["feedback"] = None # Reset feedback

        if feedback == "approved":
            shared["final_result"] = shared.get("processed_output")
            print("ReviewNode Post: Action=approved")
            return "approved"
        else:
            print("ReviewNode Post: Action=rejected")
            return "rejected"

class ResultNode(Node):
     def prep(self, shared):
         print("ResultNode Prep")
         return shared.get("final_result", "No final result.")

     def exec(self, prep_res):
         print(f"--- FINAL RESULT ---")
         print(prep_res)
         print(f"--------------------")
         return prep_res

     def post(self, shared, prep_res, exec_res):
         print("ResultNode Post: Flow finished.")
         return None # End flow