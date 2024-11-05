import { Card, Typography, Carousel } from "antd";
const { Title } = Typography;
export default function ProductItem({
  name,
  images,

}: any) {
  return (
    <div className="flex-grow flex flex-col gap-4 w-[48%]">
      <Card
        cover={
          <div className="relative p-3">
            {/* Product Image */}
            <Carousel>
              {images.map((imgSrc: string, index: Number) => (
                <img
                  key={index.toString()}
                  src={imgSrc}
                  alt={`${name} - image`}
                  style={{
                    width: "100%",
                    height: "240px",
                    objectFit: "cover",
                    borderRadius: "16px",
                    padding: "10px",
                  }}
                  className=""
                />
              ))}
            </Carousel>
            {/* Tag for special features */}
            {/* <Tag
              color="blue"
              style={{
                position: "absolute",
                top: "20px",
                left: "20px",
                fontSize: "12px",
                fontWeight: "bold",
              }}
            >
              {mattressInABox === "Yes" ? "Box" : "No Box"}
            </Tag> */}
          </div>
        }
        className="cursor-pointer border border-gray-400 hover:border-gray-800"
      >
        {/* Product Info */}
        <Title level={5}>{name}</Title>
        {/* <div style={{ marginBottom: "4px" }}>
          <ConfigProvider
            theme={{
              token: {
                marginXS: 1,
              },
            }}
          >
            <Rate
              disabled
              allowHalf
              value={rating}
              className="text-xs mr-2 text-black"
            />
          </ConfigProvider>

          <span className="text-xs">({numReviews})</span>
        </div> */}
        {/* <div className="flex justify-between items-center">
          <div>
            <span className="mb-0 text-sm font-medium">{size}</span>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                marginTop: "8px",
              }}
            >
              <span className="text-[#cf4235] text-lg font-bold mr-2">
                ${currentPrice}
              </span>
            </div>
          </div>
          <div>
            <div className="font-semibold mb-0">
              {comfort},{mattressType}
            </div>

            <span className="font-medium">Best for</span>
            <ul className="list-disc list-inside mt-1 ml-3 text-xs">
              <li>{bestFor}</li>
              <li>{pressureRelief ? "Pressure Relief" : null}</li>
              <li>{support ? "Support" : null}</li>
            </ul>
          </div>
        </div> */}
      </Card>
    </div>
  );
}
