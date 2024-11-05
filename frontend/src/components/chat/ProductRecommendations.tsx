import { useProductStore } from "../../store/chatStore";
import ProductItem from "./ProductItem";

export default function ProductRecommendations() {
  const { productObjects } = useProductStore();

  const listProducts: JSX.Element[] = productObjects.map((object, index) => {
    if (typeof object === "object") {
      return (
        <ProductItem
          name={object.name}
          images={object.images}
          currentPrice={object.current_price}
          rating={object.rating}
          numReviews={object.num_reviews}
          comfort={object.comfort}
          bestFor={object.best_for}
          mattressType={object.mattress_type}
          height={object.height}
          coolingTechnology={object.cooling_technology}
          motionSeparation={object.motion_separation}
          pressureRelief={object.pressure_relief}
          support={object.support}
          adjustableBaseFriendly={object.adjustable_base_friendly}
          breathable={object.breathable}
          mattressInABox={object.mattress_in_a_box}
          size={object.size}
          key={index}
        />
      );
    } else return <></>;
  });

  return (
    <div className="h-[96%]">
      <h2 className="font-bold text-lg text-gray-700 mb-2">
        Recommended Products
      </h2>
      <p className="text-gray-500 mb-6">
        Select one or more mattresses to refine your choices.
      </p>
      <div className="flex flex-wrap gap-4 justify-between mb-2 h-full overflow-y-auto pr-4 scrollbar-custom">
        {/* {demoProducts.map((product, index) => (
          <ProductItem
            key={index}
            name={product.name}
            images={product.images}
            currentPrice={product.current_price}
            rating={product.rating}
            numReviews={product.num_reviews}
            comfort={product.comfort}
            bestFor={product.best_for}
            mattressType={product.mattress_type}
            height={product.height}
            coolingTechnology={product.cooling_technology}
            motionSeparation={product.motion_separation}
            pressureRelief={product.pressure_relief}
            support={product.support}
            adjustableBaseFriendly={product.adjustable_base_friendly}
            breathable={product.breathable}
            mattressInABox={product.mattress_in_a_box}
            size={product.size}
            selected={product.selected}
          />
        ))} */}
        {listProducts}
        <div className="pt-10 pb-4 px-0"></div>
      </div>
      {listProducts}
    </div>
  );
}
