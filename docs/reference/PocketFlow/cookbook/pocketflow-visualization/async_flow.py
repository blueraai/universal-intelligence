from pocketflow import AsyncNode, AsyncFlow
import asyncio


# Define Payment Nodes
class ValidatePayment(AsyncNode):
    async def exec_async(self, prep_res):
        print("1.1.Validating payment...")
        return "Payment validated successfully"

    async def post_async(self, shared, prep_res, exec_res):
        shared["payment_status"] = exec_res
        return "default"


class ProcessPayment(AsyncNode):
    async def exec_async(self, prep_res):
        print("1.2.Processing payment...")
        return "Payment processed successfully"

    async def post_async(self, shared, prep_res, exec_res):
        shared["payment_result"] = exec_res
        return "default"


class PaymentConfirmation(AsyncNode):
    async def exec_async(self, prep_res):
        print("1.3.Confirming payment...")
        return "Payment confirmed"

    async def post_async(self, shared, prep_res, exec_res):
        shared["payment_confirmation"] = exec_res
        return "default"


# Define Inventory Nodes
class CheckStock(AsyncNode):
    async def exec_async(self, prep_res):
        print("2.1.Checking inventory stock...")
        return "Stock available"

    async def post_async(self, shared, prep_res, exec_res):
        shared["stock_status"] = exec_res
        return "default"


class ReserveItems(AsyncNode):
    async def exec_async(self, prep_res):
        print("2.2.Reserving items...")
        return "Items reserved"

    async def post_async(self, shared, prep_res, exec_res):
        shared["reservation_status"] = exec_res
        return "default"


class UpdateInventory(AsyncNode):
    async def exec_async(self, prep_res):
        print("2.3. Updating inventory...")
        return "Inventory updated"

    async def post_async(self, shared, prep_res, exec_res):
        shared["inventory_update"] = exec_res
        return "default"


# Define Shipping Nodes
class CreateLabel(AsyncNode):
    async def exec_async(self, prep_res):
        print("3.1 Creating shipping label...")
        return "Shipping label created"

    async def post_async(self, shared, prep_res, exec_res):
        shared["shipping_label"] = exec_res
        return "default"


class AssignCarrier(AsyncNode):
    async def exec_async(self, prep_res):
        print("3.2 Assigning carrier...")
        return "Carrier assigned"

    async def post_async(self, shared, prep_res, exec_res):
        shared["carrier"] = exec_res
        return "default"


class SchedulePickup(AsyncNode):
    async def exec_async(self, prep_res):
        print("3.3 Scheduling pickup...")
        return "Pickup scheduled"

    async def post_async(self, shared, prep_res, exec_res):
        shared["pickup_status"] = exec_res
        return "default"


# Create node instances
validate_payment = ValidatePayment()
process_payment = ProcessPayment()
payment_confirmation = PaymentConfirmation()

check_stock = CheckStock()
reserve_items = ReserveItems()
update_inventory = UpdateInventory()

create_label = CreateLabel()
assign_carrier = AssignCarrier()
schedule_pickup = SchedulePickup()

# Payment processing sub-flow
validate_payment >> process_payment >> payment_confirmation
payment_flow = AsyncFlow(start=validate_payment)

# Inventory sub-flow
check_stock >> reserve_items >> update_inventory
inventory_flow = AsyncFlow(start=check_stock)

# Shipping sub-flow
create_label >> assign_carrier >> schedule_pickup
shipping_flow = AsyncFlow(start=create_label)

# Connect the flows into a main order pipeline
payment_flow >> inventory_flow >> shipping_flow
# payment_flow >> inventory_flow >> create_label
# payment_flow >> inventory_flow >> assign_carrier


# Create the master flow
class OrderFlow(AsyncFlow):
    pass


order_pipeline = OrderFlow(start=payment_flow)

# Create shared data structure
shared_data = {
    "order_id": "ORD-12345",
    "customer": "John Doe",
    "items": [
        {"id": "ITEM-001", "name": "Smartphone", "price": 999.99, "quantity": 1},
        {"id": "ITEM-002", "name": "Phone case", "price": 29.99, "quantity": 1},
    ],
    "shipping_address": {
        "street": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip": "12345",
    },
}


# Run the entire pipeline asynchronously
async def main():
    await order_pipeline.run_async(shared_data)

    # Print final status
    print("\nOrder processing completed!")
    print(f"Payment: {shared_data.get('payment_confirmation')}")
    print(f"Inventory: {shared_data.get('inventory_update')}")
    print(f"Shipping: {shared_data.get('pickup_status')}")


if __name__ == "__main__":
    asyncio.run(main())
