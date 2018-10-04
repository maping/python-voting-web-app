package ms.kenchen.Calculator;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;
import java.util.Date;
import java.lang.Math;

@Path("/calculator")
public class CalculatorService {
    @GET
    @Path("ping")
    @Produces(MediaType.TEXT_PLAIN)
    public String ping() {
        return "Welcome to Java Web API on ACS v9!\n" + new Date().toString();
    }

    @GET
    @Path("add")
    @Produces(MediaType.APPLICATION_JSON)
    public CalculatorResponse Add(@QueryParam("x") int x, @QueryParam("y") int y) {
        return new CalculatorResponse(x, y, x + y);
    }

    @GET
    @Path("sub")
    @Produces(MediaType.APPLICATION_JSON)
    public CalculatorResponse Sub(@QueryParam("x") int x, @QueryParam("y") int y) {
        return new CalculatorResponse(x, y, x - y);
    }

    @GET
    @Path("mul")
    @Produces(MediaType.APPLICATION_JSON)
    public CalculatorResponse Mul(@QueryParam("x") int x, @QueryParam("y") int y) {
        return new CalculatorResponse(x, y, x * y);
    }

    @GET
    @Path("div")
    @Produces(MediaType.APPLICATION_JSON)
    public CalculatorResponse Div(@QueryParam("x") int x, @QueryParam("y") int y) {
        return new CalculatorResponse(x, y, x / y);
    }

    @GET
    @Path("max")
    @Produces(MediaType.APPLICATION_JSON)
    public CalculatorResponse Max(@QueryParam("x") int x, @QueryParam("y") int y) {
        return new CalculatorResponse(x, y, Math.max(x, y));
    }
}
